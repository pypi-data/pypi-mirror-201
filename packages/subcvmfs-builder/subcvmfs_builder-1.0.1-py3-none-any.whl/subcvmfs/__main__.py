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
Entrypoint module: defines the CLI.
"""


import argparse
import logging
import logging.config
from pathlib import Path
import sys
from typing import Optional

from .checkers import (
    apps_dir_valid,
    number_cores_valid,
    path_list_valid,
    config_valid,
    subset_path_valid,
    logging_config_valid,
)
from .config import get_step_param, get_tool_param, get_repositories_params
from .steps import trace, build, test, deploy


def parse_args():
    """Parse the arguments of subcvmfs-builder"""
    parser = argparse.ArgumentParser(description="Parser for SubCVMFS-Builder")
    subparsers = parser.add_subparsers(help="Create a subset of CVMFS")

    # Trace cli
    parser_trace = subparsers.add_parser("trace", help="Trace applications of interest")
    parser_trace.add_argument(
        "config", help="configuration of CVMFS repositories as input"
    )
    parser_trace.add_argument("--apps-dir", help="directory of applications")
    parser_trace.add_argument(
        "--number-cores", type=int, help="number of cores to employ in parallel"
    )
    parser_trace.add_argument(
        "--http-proxy",
        help="http proxy to trace dependencies of applications from CVMFS",
    )
    parser_trace.add_argument(
        "--container", help="container in which applications should be traced"
    )
    parser_trace.add_argument(
        "--path-list", help="file containing paths involved in the executions as output"
    )
    parser_trace.set_defaults(func=trace_cli)

    # Build cli
    parser_build = subparsers.add_parser(
        "build", help="Build a subset of CVMFS based on lists of files"
    )
    parser_build.add_argument(
        "config", help="configuration of CVMFS repositories as input"
    )
    parser_build.add_argument(
        "--path-list",
        nargs="+",
        help="file containing list of paths to add to the subset as input",
    )
    parser_build.add_argument(
        "--subset-path", help="path to the generated subset of CVMFS"
    )
    parser_build.set_defaults(func=build_cli)

    # Test cli
    parser_test = subparsers.add_parser(
        "test", help="Test applications of interest against a given subset"
    )
    parser_test.add_argument(
        "config", help="configuration of CVMFS repositories as input"
    )
    parser_test.add_argument("--apps-dir", help="directory of applications as input")
    parser_test.add_argument(
        "--number-cores", type=int, help="number of cores to employ in parallel"
    )
    parser_test.add_argument("--subset-path", help="path to a subset of CVMFS")
    parser_test.add_argument(
        "--container", help="container in which applications should be tested"
    )
    parser_test.set_defaults(func=test_cli)

    # Deploy cli
    parser_deploy = subparsers.add_parser(
        "deploy", help="Deploy subset of CVMFS on a remote machine"
    )
    parser_deploy.add_argument(
        "config", help="configuration of CVMFS repositories as input"
    )
    parser_deploy.add_argument("--subset-path", help="path to a subset of CVMFS")
    parser_deploy.add_argument(
        "--remote-location", help="remote location to install the subset"
    )
    parser_deploy.add_argument(
        "--bundle-path", help="path to a container bundling the subset"
    )
    parser_deploy.add_argument(
        "--container", help="container that will embed the subset"
    )
    parser_deploy.add_argument("--bootstrap", help="container type")
    parser_deploy.add_argument(
        "--post-command", help="container post command to include in bundle"
    )
    parser_deploy.set_defaults(func=deploy_cli)

    args = parser.parse_args()
    if hasattr(args, "func") and args.func:
        args.func(args)
    else:
        parser.print_help()

    # Explicitly exit to make testing easier
    sys.exit(0)


def trace_cli(args):
    """Get and check the validity of the inputs"""
    config_dict, command_outputs = initialize(args.config, "trace")
    if not config_dict:
        sys.exit(1)

    # Get inputs and valid them
    apps_dir = get_step_param(config_dict, "trace", "apps_dir", args.apps_dir)
    if not apps_dir_valid(apps_dir):
        sys.exit(1)

    number_cores = get_step_param(
        config_dict, "trace", "number_cores", args.number_cores
    )
    if not number_cores_valid(number_cores):
        sys.exit(1)
    if not number_cores:
        number_cores = 1

    repositories = get_repositories_params(config_dict)

    http_proxy = get_tool_param(config_dict, "parrot", "http_proxy", args.http_proxy)
    if not http_proxy:
        logging.error(f"{http_proxy} is not defined")
        sys.exit(1)

    container = get_tool_param(config_dict, "singularity", "name", args.container)
    if not container:
        logging.error(f"{container} is not defined")
        sys.exit(1)

    # Get output and valid it
    path_list = get_step_param(config_dict, "trace", "path_list", args.path_list)
    if not path_list:
        logging.error(f"{path_list} is not defined")
        sys.exit(1)

    result = trace(
        apps_dir,
        repositories,
        http_proxy,
        container,
        path_list,
        number_cores,
        command_outputs,
    )
    if not result:
        logging.error("Trace operation failed")
        sys.exit(1)


def build_cli(args):
    """Get and check the validity of the inputs"""
    config_dict, command_outputs = initialize(args.config, "build")
    if not config_dict:
        sys.exit(1)

    # Get inputs and valid them
    path_list = get_step_param(config_dict, "build", "path_list", args.path_list)
    if isinstance(path_list, str):
        path_list = [path_list]

    for path_list_file in path_list:
        if not path_list_valid(path_list_file):
            sys.exit(1)

    repositories = get_repositories_params(config_dict)

    # Get output and valid it
    subset_path = get_step_param(config_dict, "build", "subset_path", args.subset_path)
    if not subset_path:
        logging.error(f"{subset_path} is not defined")
        sys.exit(1)

    result = build(path_list, repositories, subset_path, command_outputs)
    if not result:
        logging.error(f"Build operation failed")
        sys.exit(1)


def test_cli(args):
    """Get and check the validity of the inputs"""
    config_dict, command_outputs = initialize(args.config, "test")
    if not config_dict:
        sys.exit(1)

    # Get inputs and valid them
    apps_dir = get_step_param(config_dict, "test", "apps_dir", args.apps_dir)
    if not apps_dir_valid(apps_dir):
        sys.exit(1)

    number_cores = get_step_param(
        config_dict, "trace", "number_cores", args.number_cores
    )
    if not number_cores_valid(number_cores):
        sys.exit(1)
    if not number_cores:
        number_cores = 1

    subset_path = get_step_param(config_dict, "test", "subset_path", args.subset_path)
    if not subset_path_valid(subset_path):
        sys.exit(1)

    container = get_tool_param(config_dict, "singularity", "name", args.container)
    if not container:
        logging.error(f"{container} is not defined")
        sys.exit(1)

    result = test(apps_dir, subset_path, container, number_cores, command_outputs)
    if not result:
        logging.error(f"Test operation failed")
        sys.exit(1)


def deploy_cli(args):
    """Get and check the validity of the inputs"""
    config_dict, command_outputs = initialize(args.config, "deploy")
    if not config_dict:
        sys.exit(1)

    # Get inputs and valid them
    subset_path = get_step_param(config_dict, "deploy", "subset_path", args.subset_path)
    if not subset_path_valid(subset_path):
        sys.exit(1)

    remote_location = get_step_param(
        config_dict, "deploy", "remote_location", args.remote_location
    )
    if not remote_location:
        sys.exit(1)

    container = get_tool_param(config_dict, "singularity", "name", args.container)
    bootstrap = get_tool_param(config_dict, "singularity", "bootsrap", args.bootstrap)
    bundle_path = get_step_param(config_dict, "deploy", "bundle_path", args.bundle_path)
    post_command = None

    if container and bootstrap and bundle_path:
        logging.info(
            f"{subset_path} is going to be merged with {container}: result will be stored in {bundle_path}"
        )
        post_command = get_tool_param(
            config_dict, "singularity", "post_command", args.post_command
        )

    result = deploy(
        subset_path,
        remote_location,
        container,
        bootstrap,
        post_command,
        bundle_path,
        command_outputs,
    )
    if not result:
        logging.error("Deploy operation failed")
        sys.exit(1)


def initialize(config: str, step: str = None) -> Optional[tuple[dict, str]]:
    """Common initialization: config and logging and command output

    :type config: str
    :param config: configuration path
    :type step: str
    :param step: name of the current step
    :return: tuple containing the configuration and the output file names
    """
    config_dict = config_valid(config)
    if not config_dict:
        return None

    # logging configuration, get yaml file from the config and use it
    logging_conf = get_tool_param(config_dict, "logging", "config_path", None)
    if logging_conf:
        logging_conf_dict = logging_config_valid(logging_conf)
        if logging_conf_dict:
            logging.config.dictConfig(logging_conf_dict)

    # command outputs should be a list such as: [out, err]
    command_outputs = get_step_param(config_dict, step, "command_outputs", None)
    if not isinstance(command_outputs, list) or len(command_outputs) != 2:
        command_outputs = None
    Path(command_outputs[0]).unlink(missing_ok=True)
    Path(command_outputs[1]).unlink(missing_ok=True)

    return (config_dict, command_outputs)


if __name__ == "__main__":
    parse_args()
