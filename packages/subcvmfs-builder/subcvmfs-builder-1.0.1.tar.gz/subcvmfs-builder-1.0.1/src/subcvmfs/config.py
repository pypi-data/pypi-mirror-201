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
Config module: interacts with the configuration file and retrieve information in the correct order.
"""


def get_step_param(config: dict, step: str, parameter: str, overload_value: str) -> str:
    """Get the parameters of a given step

    :type config: dict
    :param config: dictionary of configuration parameters
    :type step: str
    :param step: name of a step
    :type parameter: str
    :param parameter: parmater from a step
    :type overload_value: str
    :param overload_value: value to return if not None
    :return: a parameter value or None if not defined
    """
    if overload_value:
        return overload_value

    if not "steps" in config:
        return None

    if not step in config["steps"] or not parameter in config["steps"][step]:
        if (
            not "commons" in config["steps"]
            or not parameter in config["steps"]["commons"]
        ):
            return None
        else:
            return config["steps"]["commons"].get(parameter)
    else:
        return config["steps"][step].get(parameter)


def get_tool_param(config: dict, tool: str, parameter: str, overload_value: str) -> str:
    """Get the parameters of a given tool

    :type config: dict
    :param config: dictionary of configuration parameters
    :type tool: str
    :param tool: name of the tool
    :type parameter: str
    :param parameter: parmater from a step
    :type overload_value: str
    :param overload_value: value to return if not None
    :return: a parameter value or None if not defined
    """
    if overload_value:
        return overload_value

    if not "tools" in config:
        return None

    if not tool in config["tools"]:
        return None

    return config["tools"][tool].get(parameter)


def get_repositories_params(config: dict) -> dict:
    """Get repositories parameters

    :type config: dict
    :param config: dictionary of configuration parameters
    :return: dict of CVMFS extensions
    """
    return config.get("cvmfs_extensions")
