# base imports
import os
import io
import requests
import pandas as pd
import getpass
import gdown
import zipfile
import boto3
import paramiko
import logging
import sys
import ftfy
import urllib
from tqdm import tqdm
from pathlib import Path
from paramiko import SFTPClient, SSHClient

# util imports
from kso_utils.project_utils import Project, find_project

# Logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


######################################
# ###### Common server functions ######
# #####################################


def connect_to_server(project: Project):
    """
    > This function connects to the server specified in the project object and returns a dictionary with
    the client and sftp client

    :param project: the project object
    :return: A dictionary with the client and sftp_client
    """
    # Get project-specific server info
    if project is None or not hasattr(project, "server"):
        logging.error("No server information found, edit projects_list.csv")
        return {}

    server = project.server

    # Create an empty dictionary to host the server connections
    server_dict = {}

    if server == "AWS":
        # Connect to AWS as a client
        client = get_aws_client()

    elif server == "SNIC":
        # Connect to SNIC as a client and get sftp
        client, sftp_client = get_snic_client()
    else:
        server_dict = {}

    if "client" in vars():
        server_dict["client"] = client

    if "sftp_client" in vars():
        server_dict["sftp_client"] = sftp_client

    return server_dict


def get_ml_data(project: Project):
    """
    It downloads the training data from Google Drive.
    Currently only applies to the Template Project as other projects do not have prepared
    training data.

    :param project: The project object that contains all the information about the project
    :type project: Project
    """
    if project.ml_folder is not None and not os.path.exists(project.ml_folder):
        # Download the folder containing the training data
        if project.server == "TEMPLATE":
            gdrive_id = "1xknKGcMnHJXu8wFZTAwiKuR3xCATKco9"
            ml_folder = project.ml_folder

            # Download template training files from Gdrive
            download_gdrive(gdrive_id, ml_folder)
            logging.info("Template data downloaded successfully")
        else:
            logging.info("No download method implemented for this data")
    else:
        logging.info("No prepared data to be downloaded.")


def update_csv_server(
    project: Project, db_info_dict: dict, orig_csv: str, updated_csv: str
):
    """
    > This function updates the original csv file with the updated csv file in the server

    :param project: the project object
    :param db_info_dict: a dictionary containing the following keys:
    :type db_info_dict: dict
    :param orig_csv: the original csv file name
    :type orig_csv: str
    :param updated_csv: the updated csv file
    :type updated_csv: str
    """
    server = project.server

    # TODO: add changes in a log file

    if server == "AWS":
        logging.info("Updating csv file in AWS server")
        # Update csv to AWS
        upload_file_to_s3(
            db_info_dict["client"],
            bucket=db_info_dict["bucket"],
            key=str(db_info_dict[orig_csv]),
            filename=str(db_info_dict[updated_csv]),
        )

    elif server == "TEMPLATE":
        logging.error(
            f"{orig_csv} couldn't be updated. Check writing permisions to the server."
        )

    elif server == "SNIC":
        # Specify volume allocated by SNIC
        snic_path = "/mimer/NOBACKUP/groups/snic2021-6-9"
        # TODO: orig_csv and updated_csv as filenames, create full path for upload_object_to_snic with project.csv_folder.
        # Use below definition for production, commented not for development
        # local_fpath = project.csv_folder + updated_csv
        # Special implementation with two dummy folders for SNIC case since local and server
        # are essentially the same for now.
        local_fpath = f"{snic_path}/tmp_dir/local_dir_dev/" + updated_csv
        remote_fpath = f"{snic_path}/tmp_dir/server_dir_dev/" + orig_csv
        upload_object_to_snic(
            sftp_client=db_info_dict["sftp_client"],
            local_fpath=local_fpath,
            remote_fpath=remote_fpath,
        )

    elif server == "LOCAL":
        logging.error("Updating csv files to the server is a work in progress")

    else:
        logging.error(
            f"{orig_csv} couldn't be updated. Check writing permisions to the server."
        )


def upload_movie_server(
    movie_path: str, f_path: str, db_info_dict: dict, project: Project
):
    """
    Takes the file path of a movie file and uploads it to the server.

    :param movie_path: The local path to the movie file you want to upload
    :type movie_path: str
    :param f_path: The server or storage path of the original movie you want to convert
    :type f_path: str
    :param db_info_dict: a dictionary with the initial information of the project
    :param project: The filename of the movie file you want to convert
    :type movie_path: str
    """
    if project.server == "AWS":
        # Retrieve the key of the movie of interest
        f_path_key = f_path.split("/").str[:2].str.join("/")
        logging.info(f_path_key)

        # Upload the movie to AWS
        # upload_file_to_s3(db_info_dict["client"],
        # bucket=db_info_dict["bucket"],
        # key=f_path_key,
        # filename=movie_path)

        # logging.info(f"{movie_path} has been added to the server")

    elif project.server == "TEMPLATE":
        logging.error(f"{movie_path} not uploaded to the server as project is template")

    elif project.server == "SNIC":
        logging.error("Uploading the movies to the server is a work in progress")

    elif project.server == "LOCAL":
        logging.error(f"{movie_path} not uploaded to the server as project is local")

    else:
        raise ValueError("Specify the server of the project in the project_list.csv.")


def get_movie_url(project: Project, server_dict: dict, f_path: str):
    """
    Function to get the url of the movie
    """
    server = project.server
    if server == "AWS":
        movie_key = urllib.parse.unquote(f_path).split("/", 3)[3]
        movie_url = server_dict["client"].generate_presigned_url(
            "get_object",
            Params={"Bucket": project.bucket, "Key": movie_key},
            ExpiresIn=86400,
        )
        return movie_url
    else:
        return f_path


#####################
# ## AWS functions ###
# ####################


def aws_credentials():
    # Save your access key for the s3 bucket.
    aws_access_key_id = getpass.getpass("Enter the key id for the aws server")
    aws_secret_access_key = getpass.getpass(
        "Enter the secret access key for the aws server"
    )

    return aws_access_key_id, aws_secret_access_key


def connect_s3(aws_access_key_id: str, aws_secret_access_key: str):
    # Connect to the s3 bucket
    client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return client


def get_aws_client():
    # Set aws account credentials
    aws_access_key_id, aws_secret_access_key = os.getenv("SPY_KEY"), os.getenv(
        "SPY_SECRET"
    )
    if aws_access_key_id is None or aws_secret_access_key is None:
        aws_access_key_id, aws_secret_access_key = aws_credentials()

    # Connect to S3
    client = connect_s3(aws_access_key_id, aws_secret_access_key)

    return client


def get_matching_s3_objects(
    client: boto3.client, bucket: str, prefix: str = "", suffix: str = ""
):
    """
    ## Code modified from alexwlchan (https://alexwlchan.net/2019/07/listing-s3-keys/)
    Generate objects in an S3 bucket.

    :param client: S3 client.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """

    paginator = client.get_paginator("list_objects_v2")

    kwargs = {"Bucket": bucket}

    # We can pass the prefix directly to the S3 API.  If the user has passed
    # a tuple or list of prefixes, we go through them one by one.
    if isinstance(prefix, str):
        prefixes = (prefix,)
    else:
        prefixes = prefix

    for key_prefix in prefixes:
        kwargs["Prefix"] = key_prefix

        for page in paginator.paginate(**kwargs):
            try:
                contents = page["Contents"]
            except KeyError:
                break

            for obj in contents:
                key = obj["Key"]
                if key.endswith(suffix):
                    yield obj


def get_matching_s3_keys(
    client: boto3.client, bucket: str, prefix: str = "", suffix: str = ""
):
    """
    ## Code from alexwlchan (https://alexwlchan.net/2019/07/listing-s3-keys/)
    Generate the keys in an S3 bucket.

    :param client: S3 client.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """

    # Select the relevant bucket
    s3_keys = [
        obj["Key"] for obj in get_matching_s3_objects(client, bucket, prefix, suffix)
    ]

    # Set the contents as pandas dataframe
    contents_s3_pd = pd.DataFrame(s3_keys, columns=["Key"])

    return contents_s3_pd


def download_csv_aws(project_name: str, server_dict: dict, db_csv_info: dict):
    """
    > The function downloads the csv files from the server and saves them in the local directory

    :param project_name: str
    :type project_name: str
    :param server_dict: a dictionary containing the server information
    :type server_dict: dict
    :param db_csv_info: the path to the folder where the csv files will be downloaded
    :type db_csv_info: dict
    :return: A dict with the bucket, key, local_sites_csv, local_movies_csv, local_species_csv,
    local_surveys_csv, server_sites_csv, server_movies_csv, server_species_csv, server_surveys_csv
    """
    # Provide bucket and key
    project = find_project(project_name=project_name)
    bucket = project.bucket
    key = project.key

    # Create db_initial_info dict
    db_initial_info = {"bucket": bucket, "key": key}

    for i in ["sites", "movies", "species", "surveys"]:
        # Get the server path of the csv
        server_i_csv = get_matching_s3_keys(
            server_dict["client"], bucket, prefix=key + "/" + i
        )["Key"][0]

        # Specify the local path for the csv
        local_i_csv = str(Path(db_csv_info, Path(server_i_csv).name))

        # Download the csv
        download_object_from_s3(
            server_dict["client"], bucket=bucket, key=server_i_csv, filename=local_i_csv
        )

        # Save the local and server paths in the dict
        local_csv_str = str("local_" + i + "_csv")
        server_csv_str = str("server_" + i + "_csv")

        db_initial_info[local_csv_str] = Path(local_i_csv)
        db_initial_info[server_csv_str] = server_i_csv

    return db_initial_info


def download_object_from_s3(
    client: boto3.client,
    *,
    bucket: str,
    key: str,
    version_id: str = None,
    filename: str,
):
    """
    Download an object from S3 with a progress bar.

    From https://alexwlchan.net/2021/04/s3-progress-bars/
    """

    # First get the size, so we know what tqdm is counting up to.
    # Theoretically the size could change between this HeadObject and starting
    # to download the file, but this would only affect the progress bar.
    kwargs = {"Bucket": bucket, "Key": key}

    if version_id is not None:
        kwargs["VersionId"] = version_id

    object_size = client.head_object(**kwargs)["ContentLength"]

    if version_id is not None:
        ExtraArgs = {"VersionId": version_id}
    else:
        ExtraArgs = None

    with tqdm(
        total=object_size,
        unit="B",
        unit_scale=True,
        desc=filename,
        position=0,
        leave=True,
    ) as pbar:
        client.download_file(
            Bucket=bucket,
            Key=key,
            ExtraArgs=ExtraArgs,
            Filename=filename,
            Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
        )


def upload_file_to_s3(client: boto3.client, *, bucket: str, key: str, filename: str):
    """
    > Upload a file to S3, and show a progress bar if the file is large enough

    :param client: The boto3 client to use
    :param bucket: The name of the bucket to upload to
    :param key: The name of the file in S3
    :param filename: The name of the file to upload
    """

    # Get the size of the file to upload
    file_size = os.stat(filename).st_size

    # Prevent issues with small files (<1MB) and tqdm
    if file_size > 1000000:
        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            desc=filename,
            position=0,
            leave=True,
        ) as pbar:
            client.upload_file(
                Filename=filename,
                Bucket=bucket,
                Key=key,
                Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
            )
    else:
        client.upload_file(
            Filename=filename,
            Bucket=bucket,
            Key=key,
        )


def delete_file_from_s3(client: boto3.client, *, bucket: str, key: str):
    """
    > Delete a file from S3.

    :param client: boto3.client - the client object that you created in the previous step
    :type client: boto3.client
    :param bucket: The name of the bucket that contains the object to delete
    :type bucket: str
    :param key: The name of the file
    :type key: str
    """
    client.delete_object(Bucket=bucket, Key=key)


# def retrieve_s3_buckets_info(client, bucket, suffix):

#     # Select the relevant bucket
#     s3_keys = [obj["Key"] for obj in get_matching_s3_objects(client=client, bucket=bucket, suffix=suffix)]

#     # Set the contents as pandas dataframe
#     contents_s3_pd = pd.DataFrame(s3_keys)

#     return contents_s3_pd


##############################
# #######SNIC functions########
# #############################


def snic_credentials():
    # Save your access key for the SNIC server.
    snic_user = getpass.getpass("Enter your username for SNIC server")
    snic_pass = getpass.getpass("Enter your password for SNIC server")
    return snic_user, snic_pass


def connect_snic(snic_user: str, snic_pass: str):
    # Connect to the SNIC server and return SSH client
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(
        hostname="129.16.125.130", port=22, username=snic_user, password=snic_pass
    )
    return client


def create_snic_transport(snic_user: str, snic_pass: str):
    # Connect to the SNIC server and return SSH client
    t = paramiko.Transport(("129.16.125.130", 22))
    t.connect(username=snic_user, password=snic_pass)
    sftp = paramiko.SFTPClient.from_transport(t)
    return sftp


def get_snic_client():
    # Set SNIC credentials
    snic_user, snic_pass = snic_credentials()

    # Connect to SNIC
    client = connect_snic(snic_user, snic_pass)
    sftp_client = create_snic_transport(snic_user, snic_pass)

    return client, sftp_client


def get_snic_files(client: SSHClient, folder: str):
    """
    Get list of movies from SNIC server using ssh client.

    :param client: SSH client (paramiko)
    """
    stdin, stdout, stderr = client.exec_command(f"ls {folder}")
    snic_df = pd.DataFrame(stdout.read().decode("utf-8").split("\n"), columns=["spath"])
    return snic_df


def download_object_from_snic(
    sftp_client: SFTPClient, remote_fpath: str, local_fpath: str = "."
):
    """
    Download an object from SNIC with progress bar.
    """

    class TqdmWrap(tqdm):
        def viewBar(self, a, b):
            self.total = int(b)
            self.update(int(a - self.n))  # update pbar with increment

    # end of reusable imports/classes
    with TqdmWrap(ascii=True, unit="b", unit_scale=True) as pbar:
        sftp_client.get(remote_fpath, local_fpath, callback=pbar.viewBar)


def upload_object_to_snic(sftp_client: SFTPClient, local_fpath: str, remote_fpath: str):
    """
    Upload an object to SNIC with progress bar.
    """

    class TqdmWrap(tqdm):
        def viewBar(self, a, b):
            self.total = int(b)
            self.update(int(a - self.n))  # update pbar with increment

    # end of reusable imports/classes
    with TqdmWrap(ascii=True, unit="b", unit_scale=True) as pbar:
        sftp_client.put(local_fpath, remote_fpath, callback=pbar.viewBar)


###################################
# #######Google Drive functions#####
# ##################################


def download_csv_from_google_drive(file_url: str):
    # Download the csv files stored in Google Drive with initial information about
    # the movies and the species

    file_id = file_url.split("/")[-2]
    dwn_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    url = requests.get(dwn_url).text.encode("ISO-8859-1").decode()
    csv_raw = io.StringIO(url)
    dfs = pd.read_csv(csv_raw)
    return dfs


def download_gdrive(gdrive_id: str, folder_name: str):
    # Specify the url of the file to download
    url_input = f"https://drive.google.com/uc?&confirm=s5vl&id={gdrive_id}"

    logging.info(f"Retrieving the file from {url_input}")

    # Specify the output of the file
    zip_file = f"{folder_name}.zip"

    # Download the zip file
    gdown.download(url_input, zip_file, quiet=False)

    # Unzip the folder with the files
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(folder_name))

    # Remove the zipped file
    os.remove(zip_file)

    # Correct the file names by using correct encoding
    fix_text_encoding(folder_name)


def fix_text_encoding(folder_name):
    """
    This function corrects for text encoding errors, which occur when there is
    for example an ä,å,ö present. It runs through all the file and folder names
    of the directory you give it. It uses the package ftfy, which recognizes
    which encoding the text has based on the text itself, and it encodes/decodes
    it to utf8.
    This function was tested on a Linux and Windows device with package version
    6.1.1. With package version 5.8 it did not work.

    This function can replace the unswedify and reswedify functions from
    koster_utils, but this is not implemented yet.
    """
    dirpaths = []
    for dirpath, dirnames, filenames in os.walk(folder_name):
        for filename in filenames:
            os.rename(
                os.path.join(dirpath, filename),
                os.path.join(dirpath, ftfy.fix_text(filename)),
            )
        dirpaths.append(dirpath)

    for dirpath in dirpaths:
        if sys.platform.startswith("win"):  # windows has different file-path formatting
            index = dirpath.rfind("\\")
        else:  # mac and linux have the same file-path formatting
            index = dirpath.rfind("/")
        old_dir = ftfy.fix_text(dirpath[:index]) + dirpath[index:]
        new_dir = ftfy.fix_text(dirpath)
        os.rename(old_dir, new_dir)
