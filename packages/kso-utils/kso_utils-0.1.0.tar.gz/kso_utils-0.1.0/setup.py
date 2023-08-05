# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kso_utils', 'kso_utils.db_starter']

package_data = \
{'': ['*'], 'kso_utils': ['db_csv_info/*']}

install_requires = \
['boto3==1.15.18',
 'dataclass-csv==1.4.0',
 'ffmpeg-python==0.2.0',
 'ffmpeg==1.4',
 'folium==0.12.1',
 'ftfy==6.1.1',
 'gdown==4.6.4',
 'imagesize==1.4.1',
 'ipyfilechooser==0.4.4',
 'ipysheet==0.4.4',
 'ipython==8.11.0',
 'ipywidgets==7.7.2',
 'jupyter-bbox-widget==0.5.0',
 'natsort==8.1.0',
 'opencv-python==4.5.4.60',
 'pandas==1.5.3',
 'panoptes-client==1.6.0',
 'paramiko==2.11.0',
 'pillow==9.4.0',
 'pims==0.6.1',
 'pyyaml==6.0',
 'requests==2.28.2',
 'scikit-learn==1.2.2',
 'scp==0.14.1',
 'split-folders==0.5.1',
 'torch==1.8.0',
 'tqdm==4.64.1',
 'wandb==0.13.2']

setup_kwargs = {
    'name': 'kso-utils',
    'version': '0.1.0',
    'description': 'A package containing utility scripts for use with KSO analysis notebooks.',
    'long_description': '# KSO - Utils\n\nThe Koster Seafloor Observatory is an open-source, citizen science and machine learning approach to analyse subsea movies.\n\n<!-- PROJECT SHIELDS -->\n<!--\n*** I\'m using markdown "reference style" links for readability.\n*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).\n*** See the bottom of this document for the declaration of the reference variables\n*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.\n*** https://www.markdownguide.org/basic-syntax/#reference-style-links\n-->\n[![Contributors][contributors-shield]][contributors-url]\n[![Forks][forks-shield]][forks-url]\n[![Stargazers][stars-shield]][stars-url]\n[![Issues][issues-shield]][issues-url]\n[![MIT License][license-shield]][license-url]\n\n![high-level][high-level-overview]\n\n## Module Overview\nThis utils module contains scripts and resources that are called by the tutorials used in the [data management module][datammodule] and [Object Detection module][objdecmodule]. \n\n![utils_module][utils_module]\n\n## Citation\n\nIf you use this code or its models in your research, please cite:\n\nAnton V, Germishuys J, Bergström P, Lindegarth M, Obst M (2021) An open-source, citizen science and machine learning approach to analyse subsea movies. Biodiversity Data Journal 9: e60548. https://doi.org/10.3897/BDJ.9.e60548\n\n## Collaborations/questions\nYou can find out more about the project at https://www.zooniverse.org/projects/victorav/the-koster-seafloor-observatory.\n\nWe are always excited to collaborate and help other marine scientists. Please feel free to [contact us](matthias.obst@marine.gu.se) with your questions.\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[contributors-shield]: https://img.shields.io/github/contributors/ocean-data-factory-sweden/kso_utils.svg?style=for-the-badge\n[contributors-url]: https://https://github.com/ocean-data-factory-sweden/kso_utils/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/ocean-data-factory-sweden/kso_utils.svg?style=for-the-badge\n[forks-url]: https://github.com/ocean-data-factory-sweden/kso_utils/network/members\n[stars-shield]: https://img.shields.io/github/stars/ocean-data-factory-sweden/kso_utils.svg?style=for-the-badge\n[stars-url]: https://github.com/ocean-data-factory-sweden/kso_utils/stargazers\n[issues-shield]: https://img.shields.io/github/issues/ocean-data-factory-sweden/kso_utils.svg?style=for-the-badge\n[issues-url]: https://github.com/ocean-data-factory-sweden/kso_utils/issues\n[license-shield]: https://img.shields.io/github/license/ocean-data-factory-sweden/kso_utils.svg?style=for-the-badge\n[license-url]: https://github.com/ocean-data-factory-sweden/kso_utils/blob/main/LICENSE.txt\n[high-level-overview]: https://github.com/ocean-data-factory-sweden/koster_data_management/blob/main/images/high-level-overview.png?raw=true "Overview of the three main modules and the components of the Koster Seafloor Observatory"\n[datammodule]: https://github.com/ocean-data-factory-sweden/koster_data_management\n[objdecmodule]: https://github.com/ocean-data-factory-sweden/koster_yolov4\n[utils_module]: https://github.com/ocean-data-factory-sweden/koster_data_management/blob/main/images/Koster_utils_module.png?raw=true\n',
    'author': 'Jurie Germishuys',
    'author_email': 'jurie.germishuys@combine.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
