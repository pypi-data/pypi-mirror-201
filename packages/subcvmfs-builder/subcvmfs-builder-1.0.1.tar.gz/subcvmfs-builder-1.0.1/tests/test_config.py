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
import pytest

from subcvmfs.config import get_step_param, get_tool_param, get_repositories_params


@pytest.mark.parametrize(
    "config, step, parameter, overload_value, expected",
    [
        ({}, "deploy", "apps_dir", None, None),
        ({"steps": {}}, "deploy", "apps_dir", "inputs", "inputs"),
        (
            {"steps": {"commons": {"apps_dir": "inputs2"}}},
            "deploy",
            "apps_dir",
            "inputs",
            "inputs",
        ),
        (
            {
                "steps": {
                    "commons": {"apps_dir": "inputs2"},
                    "deploy": {"apps_dir": "inputs3"},
                }
            },
            "deploy",
            "apps_dir",
            "inputs",
            "inputs",
        ),
        (
            {
                "steps": {
                    "commons": {"apps_dir": "inputs2"},
                    "deploy": {"apps_dir": "inputs3"},
                }
            },
            "deploy",
            "apps_dir",
            None,
            "inputs3",
        ),
        (
            {"steps": {"commons": {"apps_dir": "inputs2"}}},
            "deploy",
            "apps_dir",
            None,
            "inputs2",
        ),
    ],
)
def test_get_step_param(config, step, parameter, overload_value, expected):
    result = get_step_param(config, step, parameter, overload_value)
    assert result == expected


@pytest.mark.parametrize(
    "config, tool, parameter, overload_value, expected",
    [
        ({}, "parrot", "http_proxy", None, None),
        ({"tools": {}}, "parrot", "http_proxy", "DIRECT", "DIRECT"),
        (
            {"tools": {"parrot": {"http_proxy": "DIRECT2"}}},
            "parrot",
            "http_proxy",
            "DIRECT",
            "DIRECT",
        ),
        (
            {"tools": {"parrot": {"http_proxy": "DIRECT2"}}},
            "parrot",
            "http_proxy",
            None,
            "DIRECT2",
        ),
    ],
)
def test_get_tool_param(config, tool, parameter, overload_value, expected):
    result = get_tool_param(config, tool, parameter, overload_value)
    assert result == expected


@pytest.mark.parametrize(
    "config, expected",
    [({}, None), ({"cvmfs_extensions": {"repo1": {}}}, ["repo1"])],
)
def test_get_repositories_params(config, expected):
    result = get_repositories_params(config)
    if result:
        assert list(result.keys()) == expected
    else:
        assert result == expected
