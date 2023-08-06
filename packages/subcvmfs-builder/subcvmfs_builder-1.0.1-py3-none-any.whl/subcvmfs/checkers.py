###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Checkers module: validates input parameters.
"""

import json
import logging
from pathlib import Path
import yaml


def apps_dir_valid(apps_dir: str) -> bool:
    """Check whether apps_dir exists and has a correct structure such as:

    <apps_dir>/<command>/command.sh

    :type apps_dir: str
    :param apps_dir: directory of applications
    :return: True/False
    """
    # apps_dir should exist
    logging.info(f"Checking {apps_dir} structure...")

    if not apps_dir:
        logging.error(f"apps-dir is not defined")
        return False

    apps_dir_path = Path(apps_dir)
    if not apps_dir_path.exists():
        logging.error(f"{apps_dir} does not exist")
        return False

    # apps_dir should be valid
    if sum(1 for x in apps_dir_path.glob("*/command.sh")) == 0:
        logging.error(
            f"{apps_dir} does not contain any valid command:\n\t{apps_dir}/<command>/command.sh"
        )
        return False

    logging.info(f"{apps_dir} is valid")
    return True


def number_cores_valid(number_cores: int) -> bool:
    """Check whether number_cores exists and is a valid integer

    :type number_cores: int
    :param number_cores: number of cores to employ
    :return: True/False
    """
    logging.info(f"Checking number of cores ({number_cores})...")

    if number_cores:
        try:
            number_cores = int(number_cores)
        except ValueError as e:
            logging.error(f"number-cores is not a valid integer")
            return False

        if number_cores < 0:
            logging.error(f"number-cores should not be negative: {number_cores}")
            return False

    logging.info(f"{number_cores} is valid")
    return True


def path_list_valid(path_list: str) -> bool:
    """Check whether path_list exists

    :type path_list: str
    :param path_list: file containing a list of paths
    :return: True/False
    """
    # path_list should exist, cannot check the content
    logging.info(f"Checking {path_list} existence...")
    path_list_path = Path(path_list)
    if not path_list_path.exists():
        logging.error(f"{path_list} does not exist")
        return False

    logging.info(f"{path_list} is valid")
    return True


def subset_path_valid(subset_path: str) -> bool:
    """Check whether subset path exists

    :type subset_path: str
    :param subset_path: path to the subset of CVMFS
    :return: True/False
    """
    # subst_path should exists
    logging.info(f"Checking {subset_path} existence...")
    subset_path = Path(subset_path)
    if not subset_path.exists():
        logging.error(f"{subset_path} does not exist")
        return False

    logging.info(f"{subset_path} is valid")
    return True


def logging_config_valid(logging_config: str) -> dict:
    """Check whether logging config exists, is a valid yaml and contains the right fields

    :type logging_config: str
    :param logging_config: configuration file to set up CVMFS shrinkwrap
    :return: configuration dictionary
    """
    # extract information from config
    logging.info(f"Checking and extract {logging_config} data...")
    try:
        with open(logging_config) as f:
            logging_config_dict = yaml.safe_load(f)
    except FileNotFoundError:
        logging.exception(f"{logging_config} does not exist")
        return {}
    except yaml.YAMLError:
        logging.exception(f"{logging_config} is not a valid YAML document")
        return {}

    logging.info(f"{logging_config} is valid")
    return logging_config_dict


def config_valid(config: str) -> dict:
    """Check whether config exists, is a valid json and contains the right field

    :type config: str
    :param config: configuration file to set up CVMFS shrinkwrap
    :return: configuration dictionary of None
    """
    # extract information from config
    logging.info(f"Checking and extract {config} data...")
    try:
        with open(config) as f:
            config_dict = json.load(f)
    except FileNotFoundError:
        logging.exception(f"{config} does not exist")
        return {}
    except json.JSONDecodeError:
        logging.exception(f"{config} is not a valid JSON document")
        return {}

    if not config_dict.get("cvmfs_extensions"):
        logging.error(f'{config} does not contain a "cvmfs_extensions" entry')
        return {}

    for repository_name, repository_content in config_dict["cvmfs_extensions"].items():
        if not repository_content.get("url"):
            logging.error(f'{repository_name} does not contain a "url" key')
            return {}
        if not repository_content.get("public_key"):
            logging.error(f'{repository_name} does not contain a "public_key" key')
            return {}

    logging.info(f"{config} is valid")
    return config_dict
