# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['database_tools',
 'database_tools.datastores',
 'database_tools.io',
 'database_tools.processing',
 'database_tools.tools']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=3.0.1,<4.0.0',
 'heartpy>=1.2.7,<2.0.0',
 'neurokit2>=0.2.1,<0.3.0',
 'numpy>=1.23.4,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.1,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'pytest>=7.2.1,<8.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tensorflow==2.9.2',
 'tqdm>=4.64.1,<5.0.0',
 'vitaldb>=1.2.10,<2.0.0',
 'wfdb>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'heartfelt-tools',
    'version': '0.8.0',
    'description': 'Extract and process photoplethysmography and arterial blood pressure data from mimic3-waveforms and vitaldb.',
    'long_description': '<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->\n<a name="readme-top"></a>\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n      \n            \n <img src="images/heartfelt-logo.png"  width="300em" height="300em"> \n\n  \n  <h1 align="center">MIMIC-III Database Tools</h1>\n\n  <p align="center">\n    For extracting and cleaning ppg and abp data from the MIMIC-III Waveforms Database.\n    <br />\n  </p>\n</div>\n\n\n\n<!-- TABLE OF CONTENTS -->\n<details>\n  <summary>Table of Contents</summary>\n  <ol>\n    <li>\n      <a href="#introduction">Introduction</a>\n    </li>\n    <li>\n      <a href="#getting-started">Getting Started</a>\n      <ul>\n        <li><a href="#prerequisites">Prerequisites</a></li>\n      </ul>\n    </li>\n    <li><a href="#usage">Usage</a></li>\n      <ul>\n        <li><a href="#poetry">Poetry</a></li>\n        <li><a href="#get-valid-records">Get Valid Records</a></li>\n        <li><a href="#build-database">Build Database</a></li>\n        <li><a href="#evaluate-dataset">Evaluate Dataset</a></li>\n        <li><a href="#generate-records">Generate Records</a></li>\n        <li><a href="#read-records">Read Records</a></li>\n      </ul>\n    <li><a href="#license">License</a></li>\n  </ol>\n</details>\n\n\n\n<!-- Introduction -->\n## Introduction\n\nThis repo contains a set of tools for extracting and cleaning photoplethysmography (ppg) and artial blood pressure (abp) waveforms from the [MIMIC-III Waveforms Database](https://physionet.org/content/mimic3wdb/1.0/) for the purpose of blood pressure estimation via deep learning. \n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n<!-- GETTING STARTED -->\n## Getting Started\n\nThis sections details the requirements to start using this library. Links are for Ubuntu installation.\n\n### Prerequisites\n\n1. Python\n```shell\nsudo apt install python3.8 -y\nsudo apt install python3.8-dev python3.8-venv -y\n\necho \'export PATH="$PATH:/home/ubuntu/.local/bin"\' >> ~/.bashrc\nsource ~/.bashrc\n\ncurl -sS https://bootstrap.pypa.io/get-pip.py | python3.8\npython3.8 -m pip install virtualenv\npython3.8 -m venv .venv/base-env\necho \'alias base-env="source ~/.venv/base-env/bin/activate"\' >> ~/.bashrc\nbase-env\n\npython3.8 -m pip install --upgrade pip\n```\n2. Poetry\n```shell\ncurl -sSL https://install.python-poetry.org | python3 -\necho \'export PATH="$PATH:$HOME/.local/bin"\' >> ~/.bashrc\nsource ~/.bashrc\n\n# Verify installation\npoetry --version\n```\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n\n\n<!-- USAGE EXAMPLES -->\n## Usage\n\n### Poetry\nThe commands below can be used to install the poetry environment, build the project, and activate the environment.\n```shell\ncd database-tools\npoetry lock\npoetry install\npoetry build\npoetry shell\n```\n\n### Create Data Directory\nThe functions in this library rely on a data folder named with the convention `data-YYYY-MM-DD`. This directory contains two additional folders, `mimic3/` and `figures/`. The `mimic3/lines/` folder is intended to hold the jsonlines files the data will initially saved to. The `mimic3/records/` folder will hold the TFRecords files generated from these jsonlines files. This will be discussed in greater depth in the <a href="#generate-records">Generate Records</a> section.\n\n### Get Valid Records\nThe class DataLocator (located in `database_tools/tools/`) is specifically written to find valid data files in the MIMIC-III Waveforms subset and create a csv of the html links for these data files. Performing this task prior to downloading is done to improve runtime and the usability of this workflow. Valid records refers to data files that contain both PPG and ABP recordings and are at least 10 minutes in length. Currently this code is only intended for the MIMIC-III Waveforms subset but will likely be adapated to allow for valid segments to be identified in the MIMIC-III Matched Subset (records are linked to clinical data). To perform an extraction the file `scripts/get-valid-segs.py` can be run (data directory and repository path must be configured manually). This function will output a csv called `valid-segments.csv` to the data directory provided. The figure below shows how these signals are located.\n\nAdd mimic3 valid segs logic figure.\n\n### Build Database\nThe class `BuildDatabase` (located in `database_tools/tools/`) downloads data from `valid-segments.csv`, extracts PPG and ABP data, and then processed it by leveraging the `SignalProcessor` class (located in `database_tools/preprocessing/`). A database can be build by running `scripts/build_database.py` (be sure to configure the paths). BuildDatabase takes a few important parameters which modify how signals are excluded and how the signals are divided prior to processing. The `win_len` parameter controls the length of each window, `fs` is the sampling rate of the data (125 Hz in the case of MIMIC-III), while `samples_per_file`, `samples_per_patient`, and `max_samples` control the size of the dataset (how many files the data is spread across, how many samples a patient can contribute, and the total number of samples in the dataset. The final parameter `config` controls the various constants of the SignalProcessor that determine the quality threshold for accepting signals. The SignalProcessor filters signals according to the figure chart below. The functions used for this filtering can be found in `database_tools/preprocessing/`. Data exctracted with this script is saved directly to the `mimic3/lines/` folder in the data directory. A file named `mimic3_stats.csv` containing the stats of every processed waveform (not just the valid ones) will also be saved to the data directory.\n\nAdd data preprocessing figure.\n\n### Evaluate Dataset\nThe class `DataEvaluator` (located in `database_tools/tools/`) reads the `mimic3_stats.csv` file from the provided data directory and outputs figures to visualize the statistics. These figures are saved directly to the `figures/` folder in the data directory in addition to be output such that they can be viewed in a Jupyter notebook. The 3D histogram are generated using the fuction `histogram3d` located in `database_tools/plotting/`.\n\n### Generate Records\nOnce data has been extracted TFRecords can be generated for training a Tensorflow model. The class `RecordsHandler` contains the method `GenerateRecords` which is used to create the TFRecords. This can be done using `scripts/generate_records.py` (paths must be configured). When calling `GenerateRecords` the size of the train, validation, and test splits, as well as the max number of samples per file and a boolean to control whether or not the data is standardized must be specified (using `sklearn.preprocessing.StandardScaler()`.\n\n### Read Records\nThe class `RecordsHandler` also contains the function `ReadRecords` which can be used to read the TFRecords into a Tensorflow `TFRecordsDataset` object. This function can be used to inspect the integrity of the dataset or for loading the dataset for model training. The number of cores and a TensorFlow `AUTOTUNE` object must be provided.\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n\n\n<!-- LICENSE -->\n## License\n\nDistributed under the MIT License. See `LICENSE.txt` for more information.\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n',
    'author': 'Cameron Johnson',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
