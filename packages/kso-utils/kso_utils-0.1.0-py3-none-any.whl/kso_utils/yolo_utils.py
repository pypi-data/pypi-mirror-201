# base imports
import glob
import os
import argparse
import time
import cv2 as cv
import numpy as np
import re
import pims
import shutil
import yaml
import pandas as pd
import logging
import datetime
import requests

from functools import partial
from tqdm import tqdm
from pathlib import Path
from collections.abc import Callable

# util imports
from kso_utils.db_utils import create_connection
from kso_utils.movie_utils import retrieve_movie_info_from_server, unswedify
from kso_utils.server_utils import get_movie_url
from kso_utils.project_utils import Project

# Logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# globals
frame_device = cv.cuda_GpuMat()

trackerTypes = [
    "BOOSTING",
    "MIL",
    "KCF",
    "TLD",
    "MEDIANFLOW",
    "GOTURN",
    "MOSSE",
    "CSRT",
]


def applyMask(frame: np.ndarray):
    """
    It takes a frame and returns a frame with the top 50 pixels and bottom 100 pixels blacked out

    :param frame: the frame to apply the mask to
    :type frame: np.ndarray
    :return: The frame with the mask applied.
    """
    h, w, c = frame.shape
    cv.rectangle(frame, (0, h), (0 + w, h - 100), 0, -1)
    cv.rectangle(frame, (0, 0), (0 + w, 50), 0, -1)
    return frame


def clearImage(frame: np.ndarray):
    """
    We take the maximum value of each channel, and then take the minimum value of the three channels.
    Then we blur the image, and then we take the maximum value of the blurred image and the value 0.5.
    Then we take the maximum value of the difference between the channel and the maximum value of the
    channel, divided by the blurred image, and the maximum value of the channel. Then we divide the
    result by the maximum value of the channel and multiply by 255

    :param frame: the image to be processed
    :return: The clear image
    """
    channels = cv.split(frame)
    # Get the maximum value of each channel
    # and get the dark channel of each image
    # record the maximum value of each channel
    a_max_dst = [float("-inf")] * len(channels)
    for idx in range(len(channels)):
        a_max_dst[idx] = channels[idx].max()

    dark_image = cv.min(channels[0], cv.min(channels[1], channels[2]))

    # Gaussian filtering the dark channel
    dark_image = cv.GaussianBlur(dark_image, (25, 25), 0)

    image_t = (255.0 - 0.95 * dark_image) / 255.0
    image_t = cv.max(image_t, 0.5)

    # Calculate t(x) and get the clear image
    for idx in range(len(channels)):
        channels[idx] = (
            cv.max(
                cv.add(
                    cv.subtract(channels[idx].astype(np.float32), int(a_max_dst[idx]))
                    / image_t,
                    int(a_max_dst[idx]),
                ),
                0.0,
            )
            / int(a_max_dst[idx])
            * 255
        )
        channels[idx] = channels[idx].astype(np.uint8)

    return cv.merge(channels)


def ProcFrames(proc_frame_func: Callable, frames_path: str):
    """
    It takes a function that processes a single frame and a path to a folder containing frames, and
    applies the function to each frame in the folder

    :param proc_frame_func: The function that will be applied to each frame
    :type proc_frame_func: Callable
    :param frames_path: The path to the directory containing the frames
    :type frames_path: str
    :return: The time it took to process all the frames in the folder, and the number of frames
    processed.
    """
    start = time.time()
    files = os.listdir(frames_path)
    for f in files:
        if f.endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
            if os.path.exists(str(Path(frames_path, f))):
                new_frame = proc_frame_func(cv.imread(str(Path(frames_path, f))))
                cv.imwrite(str(Path(frames_path, f)), new_frame)
            else:
                new_frame = proc_frame_func(
                    cv.imread(unswedify(str(Path(frames_path, f))))
                )
                cv.imwrite(str(Path(frames_path, f)), new_frame)
    end = time.time()
    return (end - start) * 1000 / len(files), len(files)


def ProcVid(proc_frame_func: Callable, vidPath: str):
    """
    It takes a function that processes a frame and a video path, and returns the average time it takes
    to process a frame and the number of frames in the video

    :param proc_frame_func: This is the function that will be called on each frame
    :type proc_frame_func: Callable
    :param vidPath: The path to the video file
    :type vidPath: str
    :return: The average time to process a frame in milliseconds and the number of frames processed.
    """
    cap = cv.VideoCapture(vidPath)
    if cap.isOpened() is False:
        print("Error opening video stream or file")
        return
    n_frames = 0
    start = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            n_frames += 1
            proc_frame_func(frame)
        else:
            break
    end = time.time()
    cap.release()
    return (end - start) * 1000 / n_frames, n_frames


def ProcFrameCuda(frame: np.ndarray, size=(416, 416), use_gpu=False):
    """
    It takes a frame, resizes it to a smaller size, converts it to RGB, and then clears it

    :param frame: the frame to be processed
    :type frame: np.ndarray
    :param size: the size of the image to be processed
    :return: the processed frame.
    """
    if use_gpu:
        frame_device.upload(frame)
        frame_device_small = cv.resize(frame_device, dsize=size)
        fg_device = cv.cvtColor(frame_device_small, cv.COLOR_BGR2RGB)
        fg_host = fg_device.download()
        return fg_host
    else:
        frame_device_small = cv.resize(frame, dsize=size)
        fg_device = cv.cvtColor(frame_device_small, cv.COLOR_BGR2RGB)
        return fg_device


def prepare(data_path, percentage_test, out_path):
    """
    It takes a path to a folder containing images, a percentage of the images to be used for testing,
    and a path to the output folder. It then creates two files, train.txt and test.txt, which contain
    the paths to the images to be used for training and testing, respectively

    :param data_path: the path to the dataset
    :param percentage_test: The percentage of the images that we want to be in the test set
    :param out_path: The path to the output directory
    """

    dataset_path = Path(data_path, "images")

    # Create and/or truncate train.txt and test.txt
    file_train = open(Path(data_path, "train.txt"), "w")
    file_test = open(Path(data_path, "test.txt"), "w")

    # Populate train.txt and test.txt
    counter = 1
    index_test = int((1 - percentage_test) / 100 * len(os.listdir(dataset_path)))
    latest_movie = ""
    for pathAndFilename in glob.iglob(os.path.join(dataset_path, "*.jpg")):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        movie_name = title.replace("_frame_*", "", regex=True)

        if counter == index_test + 1:
            if movie_name != latest_movie:
                file_test.write(out_path + os.path.basename(title) + ".jpg" + "\n")
            else:
                file_train.write(out_path + os.path.basename(title) + ".jpg" + "\n")
            counter += 1
        else:
            latest_movie = movie_name
            file_train.write(out_path + os.path.basename(title) + ".jpg" + "\n")
            counter += 1


# utility functions
def process_frames(frames_path: str, size: tuple = (416, 416)):
    """
    It takes a path to a directory containing frames, and returns a list of processed frames

    :param frames_path: the path to the directory containing the frames
    :param size: The size of the image to be processed
    """
    # Run tests
    gpu_time_0, n_frames = ProcFrames(partial(ProcFrameCuda, size=size), frames_path)
    logging.info(
        f"Processing performance: {n_frames} frames, {gpu_time_0:.2f} ms/frame"
    )


def process_path(path: str):
    """
    Process a single path
    """
    return os.path.basename(re.split("_[0-9]+", path)[0]).replace("_frame", "")


def clean_species_name(species_name: str):
    """
    Clean species name
    """
    return species_name.lower().replace(" ", "_").replace("-", "_").replace("/", "_")


def split_frames(data_path: str, perc_test: float):
    """
    Split frames into train and test sets
    """
    dataset_path = Path(data_path)
    images_path = Path(dataset_path, "images")

    # Create and/or truncate train.txt and test.txt
    file_train = open(Path(data_path, "train.txt"), "w")
    # file_test = open(Path(data_path, "test.txt"), "w")
    file_valid = open(Path(data_path, "valid.txt"), "w")

    # Populate train.txt and test.txt
    counter = 1
    index_test = int(
        (1 - perc_test)
        * len([s for s in os.listdir(images_path) if s.endswith(".jpg")])
    )
    latest_movie = ""
    for pathAndFilename in glob.iglob(os.path.join(images_path, "*.jpg")):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        movie_name = title.replace("_frame_*", "")

        if counter >= index_test + 1:
            # Avoid leaking frames into test set
            if movie_name != latest_movie or movie_name == title:
                file_valid.write(pathAndFilename + "\n")
            else:
                file_train.write(pathAndFilename + "\n")
            counter += 1
        else:
            latest_movie = movie_name
            # if random.uniform(0, 1) <= 0.5:
            #    file_train.write(pathAndFilename + "\n")
            # else:
            file_train.write(pathAndFilename + "\n")
            counter += 1


def frame_aggregation(
    project: Project,
    db_info_dict: dict,
    out_path: str,
    perc_test: float,
    class_list: list,
    img_size: tuple,
    out_format: str = "yolo",
    remove_nulls: bool = True,
    track_frames: bool = True,
    n_tracked_frames: int = 10,
    agg_df: pd.DataFrame = pd.DataFrame(),
):
    """
    It takes a project, a database, an output path, a percentage of frames to use for testing, a list of
    species to include, an image size, an output format, a boolean to remove null annotations, a boolean
    to track frames, and the number of frames to track, and it returns a dataset of frames with bounding
    boxes for the specified species

    :param project: the project object
    :param db_info_dict: a dictionary containing the path to the database and the database name
    :type db_info_dict: dict
    :param out_path: the path to the folder where you want to save the dataset
    :type out_path: str
    :param perc_test: The percentage of frames that will be used for testing
    :type perc_test: float
    :param class_list: list of species to include in the dataset
    :type class_list: list
    :param img_size: tuple, the size of the images to be used for training
    :type img_size: tuple
    :param out_format: str = "yolo", defaults to yolo
    :type out_format: str (optional)
    :param remove_nulls: Remove null annotations from the dataset, defaults to True
    :type remove_nulls: bool (optional)
    :param track_frames: If True, the script will track the bounding boxes for n_tracked_frames frames
    after the object is detected, defaults to True
    :type track_frames: bool (optional)
    :param n_tracked_frames: number of frames to track after an object is detected, defaults to 10
    :type n_tracked_frames: int (optional)
    """
    # Establish connection to database
    conn = create_connection(db_info_dict["db_path"])

    # Select the id/s of species of interest
    if class_list[0] == "":
        logging.error(
            "No species were selected. Please select at least one species before continuing."
        )
        return

    # Select the aggregated classifications from the species of interest
    train_rows = agg_df

    # Rename columns if in different format
    train_rows = train_rows.rename(
        columns={"x": "x_position", "y": "y_position", "w": "width", "h": "height"}
    ).copy()

    # Remove null annotations
    if remove_nulls:
        train_rows = train_rows.dropna(
            subset=["x_position", "y_position", "width", "height"],
        ).copy()

    # Check if any frames are left after removing null values
    if len(train_rows) == 0:
        logging.error("No frames left. Please adjust aggregation parameters.")
        return

    # Create output folder
    if os.path.isdir(out_path):
        shutil.rmtree(out_path)
    os.mkdir(out_path)

    # Set up directory structure
    img_dir = Path(out_path, "images")
    label_dir = Path(out_path, "labels")

    # Create image and label directories
    os.mkdir(img_dir)
    os.mkdir(label_dir)

    # Create timestamped koster yaml file with model configuration
    species_list = [clean_species_name(sp) for sp in class_list]

    # Write config file
    data = dict(
        path=out_path,
        train="train.txt",
        val="valid.txt",
        nc=len(class_list),
        names=species_list,
    )

    with open(
        Path(
            out_path,
            f"{project.Project_name+'_'+datetime.datetime.now().strftime('%H:%M:%S')}.yaml",
        ),
        "w",
    ) as outfile:
        yaml.dump(data, outfile, default_flow_style=None)

    # Write hyperparameters default file (default hyperparameters from https://github.com/ultralytics/yolov5/blob/master/data/hyps/hyp.scratch.yaml)
    hyp_data = dict(
        lr0=0.01,  # initial learning rate (SGD=1E-2, Adam=1E-3)
        lrf=0.1,  # final OneCycleLR learning rate (lr0 * lrf)
        momentum=0.937,  # SGD momentum/Adam beta1
        weight_decay=0.0005,  # optimizer weight decay 5e-4
        warmup_epochs=3.0,  # warmup epochs (fractions ok)
        warmup_momentum=0.8,  # warmup initial momentum
        warmup_bias_lr=0.1,  # warmup initial bias lr
        box=0.05,  # box loss gain
        cls=0.5,  # cls loss gain
        cls_pw=1.0,  # cls BCELoss positive_weight
        obj=1.0,  # obj loss gain (scale with pixels)
        obj_pw=1.0,  # obj BCELoss positive_weight
        iou_t=0.20,  # IoU training threshold
        anchor_t=4.0,  # anchor-multiple threshold
        # anchors= 3  # anchors per output layer (0 to ignore)
        fl_gamma=0.0,  # focal loss gamma (efficientDet default gamma=1.5)
        hsv_h=0.015,  # image HSV-Hue augmentation (fraction)
        hsv_s=0.7,  # image HSV-Saturation augmentation (fraction)
        hsv_v=0.4,  # image HSV-Value augmentation (fraction)
        degrees=0.0,  # image rotation (+/- deg)
        translate=0.1,  # image translation (+/- fraction)
        scale=0.5,  # image scale (+/- gain)
        shear=0.0,  # image shear (+/- deg)
        perspective=0.0,  # image perspective (+/- fraction), range 0-0.001
        flipud=0.0,  # image flip up-down (probability)
        fliplr=0.5,  # image flip left-right (probability)
        mosaic=1.0,  # image mosaic (probability)
        mixup=0.0,  # image mixup (probability)
        copy_paste=0.0,  # segment copy-paste (probability)
    )

    with open(Path(out_path, "hyp.yaml"), "w") as outfile:
        yaml.dump(hyp_data, outfile, default_flow_style=None)

    # Clean species names
    species_df = pd.read_sql_query("SELECT id, label FROM species", conn)
    species_df["clean_label"] = species_df.label.apply(clean_species_name)

    # Add species_id to train_rows
    if not "species_id" in train_rows.columns:
        train_rows["species_id"] = train_rows["label"].apply(
            lambda x: species_df[species_df.label == x].id.values[0], 1
        )
        train_rows.drop(columns=["label"], axis=1, inplace=True)

    sp_id2mod_id = {
        species_df[species_df.clean_label == species_list[i]].id.values[0]: i
        for i in range(len(species_list))
    }

    # Get movie info from server
    movie_df = retrieve_movie_info_from_server(
        project=project, db_info_dict=db_info_dict
    )

    # If at least one movie is linked to the project
    logging.info(f"There are {len(movie_df)} movies")

    if len(movie_df) > 0:
        if (
            "frame_number" in train_rows.columns
            and not pd.isnull(train_rows["frame_number"]).any()
        ):
            movie_bool = True
        else:
            logging.info(
                "There are movies available, but the subject metadata does not contain frame "
                "numbers and will therefore not be used."
            )
            movie_bool = False
    else:
        movie_bool = False

    link_bool = "https_location" in train_rows.columns
    image_bool = project.photo_folder is not None

    if not any([movie_bool, link_bool, image_bool]):
        logging.error(
            "No source of footage for aggregation found. Please check your metadata "
            "and project setup before running this function again."
        )
        return None

    if movie_bool:
        # Get movie path on the server
        train_rows["movie_path"] = train_rows.merge(
            movie_df, left_on="movie_id", right_on="id", how="left"
        )["spath"]

        train_rows["movie_path"] = train_rows["movie_path"].apply(
            lambda x: get_movie_url(project, db_info_dict, x)
        )

        # Read each movie for efficient frame access
        video_dict = {}
        for i in tqdm(train_rows["movie_path"].unique()):
            try:
                video_dict[i] = pims.MoviePyReader(i)
            except FileNotFoundError:
                try:
                    video_dict[unswedify(str(i))] = pims.Video(unswedify(str(i)))
                except KeyError:
                    logging.warning("Missing file" + f"{i}")

        # Create full rows
        train_rows = train_rows.sort_values(
            by=["movie_path", "frame_number"], ascending=True
        )

        # Ensure key fields wrt movies are available
        key_fields = [
            "species_id",
            "frame_number",
            "movie_path",
            "x_position",
            "y_position",
            "width",
            "height",
        ]

    else:
        if link_bool:
            key_fields = [
                "subject_ids",
                "species_id",
                "x_position",
                "y_position",
                "width",
                "height",
            ]
        else:
            key_fields = [
                "species_id",
                "filename",
                "x_position",
                "y_position",
                "width",
                "height",
            ]

    # Get relevant fields from dataframe (before groupby)
    train_rows = train_rows[key_fields]

    group_fields = (
        ["subject_ids", "species_id"]
        if link_bool
        else (
            ["movie_path", "frame_number", "species_id"]
            if movie_bool
            else ["filename", "species_id"]
        )
    )

    new_rows = []
    bboxes = {}
    tboxes = {}

    for name, group in tqdm(train_rows.groupby(group_fields)):
        grouped_fields = name[: len(group_fields)]
        if not movie_bool:
            # Get the filenames of the images
            filename = (
                agg_df[agg_df.subject_ids == grouped_fields[0]]["https_location"].iloc[
                    0
                ]
                if link_bool
                else project.photo_folder + grouped_fields[0]
            )
            named_tuple = tuple([grouped_fields[1], filename])
        else:
            # Get movie_path and frame_number
            rev_fields = grouped_fields.reverse()
            named_tuple = tuple([rev_fields])

        if movie_bool:
            final_name = name[0] if name[0] in video_dict else unswedify(name[0])

            if grouped_fields[1] > len(video_dict[final_name]):
                logging.warning(
                    f"Frame out of range for video of length {len(video_dict[final_name])}"
                )

            if final_name in video_dict:
                bboxes[named_tuple], tboxes[named_tuple] = [], []
                bboxes[named_tuple].extend(
                    tuple(i[len(grouped_fields) :]) for i in group.values
                )
                movie_w, movie_h = video_dict[final_name][0].shape

                for box in bboxes[named_tuple]:
                    new_rows.append(
                        (
                            grouped_fields[-1],
                            grouped_fields[1],
                            grouped_fields[0],
                            movie_h,
                            movie_w,
                        )
                        + box
                    )

                if track_frames:
                    # Track n frames after object is detected
                    tboxes[named_tuple].extend(
                        track_objects(
                            video_dict[final_name],
                            grouped_fields[-1],
                            bboxes[named_tuple],
                            grouped_fields[1],
                            grouped_fields[1] + n_tracked_frames,
                        )
                    )
                    for box in tboxes[named_tuple]:
                        new_rows.append(
                            (
                                grouped_fields[-1],
                                grouped_fields[1] + box[0],
                                grouped_fields[-1],
                                video_dict[final_name][grouped_fields[1]].shape[1],
                                video_dict[final_name][grouped_fields[1]].shape[0],
                            )
                            + box[1:]
                        )
        else:
            # Track intermediate frames
            bboxes[named_tuple] = []
            bboxes[named_tuple].extend(
                tuple(i[len(grouped_fields) :]) for i in group.values
            )

            for box in bboxes[named_tuple]:
                new_rows.append(
                    (
                        grouped_fields[-1],  # species_id
                        filename,
                        Image.open(requests.get(filename, stream=True).raw).size[0]
                        if link_bool
                        else PIL.Image.open(filename).size[0],
                        Image.open(requests.get(filename, stream=True).raw).size[1]
                        if link_bool
                        else PIL.Image.open(filename).size[1],
                    )
                    + box
                )

    ### Final export step
    if movie_bool:
        # Export full rows
        full_rows = pd.DataFrame(
            new_rows,
            columns=[
                "species_id",
                "frame_number",
                "filename",
                "f_w",
                "f_h",
                "x",
                "y",
                "w",
                "h",
            ],
        )
        f_group_fields = ["frame_number", "filename"]
    else:
        full_rows = pd.DataFrame(
            new_rows,
            columns=[
                "species_id",
                "filename",
                "f_w",
                "f_h",
                "x",
                "y",
                "w",
                "h",
            ],
        )
        f_group_fields = ["filename"]

    # Find indices of important fields
    col_list = list(full_rows.columns)
    fw_pos, fh_pos, x_pos, y_pos, w_pos, h_pos, speciesid_pos = (
        col_list.index("f_w"),
        col_list.index("f_h"),
        col_list.index("x"),
        col_list.index("y"),
        col_list.index("w"),
        col_list.index("h"),
        col_list.index("species_id"),
    )

    for name, groups in tqdm(
        full_rows.groupby(f_group_fields),
        desc="Saving frames...",
        colour="green",
    ):
        if movie_bool:
            file, ext = os.path.splitext(name[1])
            file_base = os.path.basename(file)
            file_out = f"{out_path}/labels/{file_base}_frame_{name[0]}.txt"
            img_out = f"{out_path}/images/{file_base}_frame_{name[0]}.jpg"
        else:
            file, ext = os.path.splitext(name)
            file_base = os.path.basename(file)
            file_out = f"{out_path}/labels/{file_base}.txt"
            img_out = f"{out_path}/images/{file_base}.jpg"

        # Added condition to avoid bounding boxes outside of maximum size of frame + added 0 class id when working with single class
        if out_format == "yolo":
            if len(groups.values) == 1 and str(groups.values[0][-1]) == "nan":
                # Empty files
                open(file_out, "w")
            else:
                groups = [i for i in groups.values if str(i[-1]) != "nan"]
                open(file_out, "w").write(
                    "\n".join(
                        [
                            "{} {:.6f} {:.6f} {:.6f} {:.6f}".format(
                                0
                                if len(class_list) == 1
                                else sp_id2mod_id[
                                    i[speciesid_pos]
                                ],  # single class vs multiple classes
                                min((i[x_pos] + i[w_pos] / 2) / i[fw_pos], 1.0),
                                min((i[y_pos] + i[h_pos] / 2) / i[fh_pos], 1.0),
                                min(i[w_pos] / i[fw_pos], 1.0),
                                min(i[h_pos] / i[fh_pos], 1.0),
                            )
                            for i in groups
                        ]
                    )
                )

        # Save frames to image files
        if movie_bool:
            save_name = name[1] if name[1] in video_dict else unswedify(name[1])
            if save_name in video_dict:
                Image.fromarray(video_dict[save_name][name[0]][:, :, [2, 1, 0]]).save(
                    img_out
                )
        else:
            if link_bool:
                image_output = Image.open(requests.get(name, stream=True).raw)
            else:
                image_output = np.asarray(PIL.Image.open(name))
            Image.fromarray(np.asarray(image_output)).save(img_out)

    logging.info("Frames extracted successfully")

    # Check that at least some frames remain after aggregation
    if len(full_rows) == 0:
        raise Exception(
            "No frames found for the selected species. Please retry with a different configuration."
        )

    # Pre-process frames
    process_frames(out_path + "/images", size=tuple(img_size))

    # Create training/test sets
    split_frames(out_path, perc_test)


def createTrackerByName(trackerType: str):
    """
    It creates a tracker based on the tracker name

    :param trackerType: The type of tracker we want to use
    :return: The tracker is being returned.
    """
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv.legacy.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv.legacy.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv.legacy.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv.legacy.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv.legacy.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv.legacy.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv.legacy.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv.legacy.TrackerCSRT_create()
    else:
        tracker = None
        logging.info("Incorrect tracker name")
        logging.info("Available trackers are:")
        for t in trackerTypes:
            logging.info(t)

    return tracker


def track_objects(
    video, class_ids: list, bboxes: list, start_frame: int, last_frame: int
):
    """
    It takes a video, a list of bounding boxes, and a start and end frame, and returns a list of tuples
    containing the frame number, and the bounding box coordinates

    :param video: the video to be tracked
    :param class_ids: The class of the object you want to track
    :param bboxes: the bounding boxes of the objects to be tracked
    :param start_frame: the frame number to start tracking from
    :param last_frame: the last frame of the video to be processed
    :return: A list of tuples, where each tuple contains the frame number, x, y, width, and height of
    the bounding box.
    """

    # Set video to load
    # colors = [(randint(0, 255)) for i in bboxes]

    # Specify the tracker type
    trackerType = "CSRT"

    # Create MultiTracker object
    multiTracker = cv.legacy.MultiTracker_create()

    # Extract relevant frame
    frame = video[start_frame]  # [0]

    # Initialize MultiTracker
    for bbox in bboxes:
        multiTracker.add(createTrackerByName(trackerType), frame, bbox)

    t_bbox = []
    t = 0
    # Process video and track objects
    for current_frame in range(start_frame + 1, last_frame + 1):
        frame = video[current_frame]  # [0]

        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)
        if success:
            t += 1
            for i, newbox in enumerate(boxes):
                t_bbox.append(
                    (t, int(newbox[0]), int(newbox[1]), int(newbox[2]), int(newbox[3]))
                )

    return t_bbox


def main():
    "Handles argument parsing and launches the correct function."
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", help="path to data folder", type=str)
    parser.add_argument(
        "perc_test", help="percentage of data to use as part of test set", type=float
    )
    parser.add_argument("out_path", help="path to save into text files", type=str)
    args = parser.parse_args()

    prepare(args.data_path, args.perc_test, args.out_path)


if __name__ == "__main__":
    main()
