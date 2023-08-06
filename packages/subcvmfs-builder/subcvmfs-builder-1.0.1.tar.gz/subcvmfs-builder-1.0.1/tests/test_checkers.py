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
import logging
import pytest

from subcvmfs.checkers import (
    apps_dir_valid,
    number_cores_valid,
    path_list_valid,
    config_valid,
    logging_config_valid,
    subset_path_valid,
)


@pytest.mark.parametrize(
    "apps_dir, expected",
    [("tests/apps_dir", True), ("tests/cvmfs", False)],
)
def test_apps_dir_valid(apps_dir, expected):
    result = apps_dir_valid(apps_dir)
    assert result == expected


@pytest.mark.parametrize(
    "number_cores, expected",
    [("", True), ("1", True), (1, True), ("test", False), (-5, False)],
)
def test_number_cores_valid(number_cores, expected):
    result = number_cores_valid(number_cores)
    assert result == expected


@pytest.mark.parametrize(
    "path_list, expected",
    [
        ("tests/apps_dir/command/command.sh", True),
        ("tests/apps_dir/donotexist.spec", False),
    ],
)
def test_path_list_valid(path_list, expected):
    result = path_list_valid(path_list)
    assert result == expected


@pytest.mark.parametrize(
    "subset_path, expected",
    [("tests/cvmfs", True), ("tests/cvm", False)],
)
def test_subset_path_valid(subset_path, expected):
    result = subset_path_valid(subset_path)
    assert result == expected


@pytest.mark.parametrize(
    "config, expected",
    [
        ("tests/configs/config1.json", True),
        ("tests/configs/donotexist", False),
        ("tests/configs/badconfig1.json", False),
        ("tests/configs/badconfig2.json", False),
        ("tests/configs/badconfig3.json", False),
        ("tests/configs/badconfig4.json", False),
    ],
)
def test_config_valid(config, expected):
    result = config_valid(config)
    assert (result != {}) == expected


@pytest.mark.parametrize(
    "config, expected, expected_level",
    [
        ("tests/logging_configs/config1.yaml", True, "DEBUG"),
        ("tests/logging_configs/donotexist", False, None),
        ("tests/logging_configs/badconfig1.yaml", False, None),
    ],
)
def test_logging_config_valid(config, expected, expected_level):
    result = logging_config_valid(config)
    assert (result != {}) == expected

    if expected:
        assert logging.getLevelName(logging.getLogger().level) == expected_level
