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
Steps module: defines the business logic of subcvmfs-builder.
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import logging
import multiprocessing
import os
from pathlib import Path
import re
import shlex
import subprocess
from typing import Optional
import uuid


def trace(
    apps_dir: str,
    repositories: dict,
    http_proxy: str,
    container: str,
    path_list: str,
    number_cores: int,
    command_outputs: Optional[list[str]] = None,
):
    """Trace applications of interests and generate a list of paths involved in the process

    :type apps_dir: str
    :param apps_dir: directory of applications structured as <apps_dir>/<command>/command.sh
    :type repositories: dict
    :param repositories: configuration of the repositories to use
    :type http_proxy: str
    :param http_proxy: http proxy used to trace CVMFS
    :type container: str
    :param container: name of the container in which applications will run
    :type path_list: str
    :param path_list: file that will contain the list of the paths involved in the executions
    :type number_cores: int
    :param number_cores: number of operations to be done in parallel
    :return: True/False
    """
    namelist_content = []

    manager = multiprocessing.Manager()
    lock = manager.Lock()  # pylint: disable=no-member
    with ProcessPoolExecutor(max_workers=number_cores) as executor:
        futures = [
            executor.submit(
                trace_a_command,
                input_command,
                repositories,
                http_proxy,
                container,
                lock,
                command_outputs,
            )
            for input_command in Path(apps_dir).glob("*/command.sh")
        ]
        for future in as_completed(futures):
            if not future.result():
                executor.shutdown(wait=False)
                return False
            namelist_content.extend(future.result())

    # Export content in path_list
    with open(path_list, "w") as f:
        for path_name in namelist_content:
            f.write(f"{path_name}\n")

    return True


def trace_a_command(
    input_command: str,
    repositories: dict,
    http_proxy: str,
    container: str,
    lock: multiprocessing.Lock,
    command_outputs: Optional[list[str]] = None,
) -> list[str]:
    """Trace an application of interest (multiprocessing)

    :type input_command: str
    :param input_command: directory containing a command and input dependencies
    :type repositories: dict
    :param repositories: configuration of the repositories to use
    :type http_proxy: str
    :param http_proxy: http proxy used to trace CVMFS
    :type container: str
    :param container: name of the container in which the application will run
    """
    logging.info(f"Start tracing {input_command}")

    # Initialize Parrot to trace applications
    namelist = Path.cwd().joinpath(f"namelist_{uuid.uuid4()}.txt")
    namelist.unlink(missing_ok=True)
    envlist = Path.cwd().joinpath(f"envlist_{uuid.uuid4()}.txt")
    envlist.unlink(missing_ok=True)
    namelist_content = []

    trace_prefix = generate_trace_prefix(repositories, http_proxy, namelist, envlist)
    logging.debug(f"Trace prefix: {trace_prefix}")

    # Generate the executable
    singularity_executable = Path.cwd().joinpath(f"singularityexec_{uuid.uuid4()}.sh")
    generate_executable(
        str(singularity_executable), input_command.resolve(), trace_prefix
    )

    # Go to the script directory to get the inputs
    current_directory = Path.cwd()
    os.chdir(str(input_command.resolve().parent))

    # Set up singularity command
    command = f"singularity exec --cleanenv "
    command += f"--bind {singularity_executable.parent.resolve()} --bind /cvmfs "
    command += f"{container} {singularity_executable}"
    logging.debug(f"Command: {command}")

    # Execute it
    result = subprocess.run(
        shlex.split(command), capture_output=(command_outputs != None)
    )
    if result.returncode != 0:
        namelist.unlink(missing_ok=True)
        envlist.unlink(missing_ok=True)
        singularity_executable.unlink()
        os.chdir(str(current_directory))
        logging.error(f"{input_command} tracing failed")
        if command_outputs:
            generate_command_outputs(
                command_outputs, result.stdout, result.stderr, lock, input_command
            )
        return []

    # Preprocess the result of the execution:
    # before:
    # <path/2> | <copy type>
    # <path/1> | <copy type>
    # after:
    # <path/1>
    # <path/2>
    with open(namelist) as f:
        for line in f:
            namelist_content.append(line.split("|")[0])

    # Clean up
    singularity_executable.unlink()
    namelist.unlink()
    envlist.unlink()
    os.chdir(str(current_directory))
    if command_outputs:
        generate_command_outputs(
            command_outputs, result.stdout, result.stderr, lock, input_command
        )
    logging.info(f"{input_command} successfully traced")
    return namelist_content


def generate_trace_prefix(
    repositories: dict, http_proxy: str, namelist: str, envlist: str
) -> str:
    """Generate a prefix to initialize Parrot to trace applications

    :type repositories: dictionary
    :param repositories: CVMFS repository details
    :type http_proxy: str
    :param http_proxy: http proxy to trace dependencies of applications from CVMFS
    :type namelist: str
    :param namelist: file name that will contain paths of the dependencies traced
    :type envlist: str
    :param envlist: file name that will contain environments variables traced
    """
    parrot_cvmfs_repo = ""
    for repository_name, repository_content in repositories.items():
        url = repository_content.get("url")
        public_key = repository_content.get("public_key")
        parrot_cvmfs_repo += f"{repository_name}:url={url},pubkey={public_key} "

    trace_prefix = f'export PARROT_CVMFS_REPO="{parrot_cvmfs_repo}"\n'
    trace_prefix += f"export PARROT_ALLOW_SWITCHING_CVMFS_REPOSITORIES=yes\n"
    trace_prefix += f'export HTTP_PROXY="{http_proxy}"\n'
    trace_prefix += f"parrot_run --name-list {namelist} --env-list {envlist} "
    return trace_prefix


# ------------------------------------------------------------------------------


def build(
    path_list: str,
    repositories: dict,
    subset_path: str,
    command_outputs: Optional[list[str]] = None,
) -> bool:
    """Build a subset of CVMFS based on a list of paths and a configuration

    :type path_list: str
    :param path_list: file containing a list of paths
    :type repositories: dictionary
    :param repositories: CVMFS repository details
    :type subset_path: str
    :param subset_path: path to the subset of CVMFS
    """
    # Aggregate list of paths in namelist_paths
    namelist_paths = []
    for path_file in path_list:
        logging.debug(f"Collect {path_file} content")
        with open(path_file) as f:
            trace = f.read()
        namelist_paths.extend(re.findall("/cvmfs/.*", trace))

    # Remove non existing paths, resolve all paths
    process_user_paths(namelist_paths)
    real_paths = get_subset_paths(namelist_paths)

    # Sort paths according to the repository they come from
    process_subset_paths(repositories, real_paths)

    # Write paths in repository specification files
    for repository_name, repository in repositories.items():

        # Build the config and spec files
        if not "paths" in repository:
            logging.warn(f"{repository_name} does not contain any path, we skip it")
            continue

        spec, config = setup_config_spec_files(repository_name, repository)

        # Generate the subset of CVMFS
        command = f"cvmfs_shrinkwrap -r {repository_name} -f {config} -t {spec} --dest-base {subset_path}"
        logging.debug(f"Command: {command}")

        result = subprocess.run(
            shlex.split(command), capture_output=(command_outputs != None)
        )
        if result.returncode != 0:
            Path(spec).unlink()
            Path(config).unlink()
            if command_outputs:
                generate_command_outputs(command_outputs, result.stdout, result.stderr)
            return False

        Path(spec).unlink()
        Path(config).unlink()
        if command_outputs:
            generate_command_outputs(command_outputs, result.stdout, result.stderr)
        logging.info(f"{subset_path} has been successfully created")

    return True


def process_user_paths(namelist_paths: list[str]):
    """Process paths added manually and ending with '*':

    :type namelist_paths: list
    :param namelist_paths: list of paths to potentially add to the subset
    """
    paths_to_remove = []
    paths_to_add = []

    for namelist_path in namelist_paths:
        parrot_path = Path(namelist_path)

        if parrot_path.name == "*":
            for subpath in parrot_path.parent.rglob("*"):
                paths_to_add.append(f"{subpath}")
            paths_to_remove.append(namelist_path)

    for path_to_remove in paths_to_remove:
        namelist_paths.remove(path_to_remove)
    for path_to_add in paths_to_add:
        namelist_paths.append(path_to_add)


def get_subset_paths(namelist_paths: list[str]) -> list[str]:
    """Get subset paths from a list of paths:
        - Remove non existing paths
        - Add symbolic link and real paths

    :type namelist_paths: list
    :param namelist_paths: list of paths to potentially add to the subset
    :return: list of paths
    """
    # Sort paths
    n_skipped = 0
    real_paths = set()

    for namelist_path in namelist_paths:
        parrot_path = Path(namelist_path)

        # Check that path exists, else it is removed
        if not parrot_path.exists():
            n_skipped += 1
            logging.debug(f"Skipped {parrot_path}")
            continue

        # Check whether path is a symlink and add it if it's the case
        real_parrot_path = parrot_path.resolve()
        real_paths.add(real_parrot_path)
        if real_parrot_path != parrot_path:
            real_paths.add(parrot_path)

        # Check whether path is part of a symlink directory
        symlink_path = real_parrot_path.parent.joinpath(parrot_path.name)
        if parrot_path != symlink_path and symlink_path.exists():
            real_paths.add(symlink_path)

    # Get total size
    total_size = 0
    for path in real_paths:
        total_size += path.stat().st_size

    logging.info(f"Skipped {n_skipped} paths that don't exist")
    logging.info(f"Found {len(real_paths)} paths that were opened")
    logging.info(f"Total size of files is {(total_size/1024**2)} MB")
    return real_paths


def process_subset_paths(repositories: dict, paths: list[str]):
    """Process path_list and store paths in repositories

    :type repositories: dict
    :param repositories: configuration parameters of repositories
    :type path_list: list
    :param path_list: list of paths to process
    """
    for real_path in paths:
        repository_name = real_path.parts[2]
        if not repository_name in repositories:
            logging.debug(f"{real_path} was found but not integrated")
            continue

        if not "paths" in repositories[repository_name]:
            repositories[repository_name]["paths"] = []

        path_to_add = Path("/").joinpath(
            real_path.relative_to(f"/cvmfs/{repository_name}")
        )
        repositories[repository_name]["paths"].append(path_to_add)


def setup_config_spec_files(
    repository_name: str, repository_content: dict
) -> tuple[str, str]:
    """Build CVMFS shrinkwrap config and spec files according to
        the repository info in parameters.

    :type repository_name: str
    :param repository_name: name of the repository
    :type repository_content: dict
    :param repository_content: parameters related to a repository
    :return: tuple combining the name of the spec and the config files
    """
    spec = f"{repository_name}.spec"
    config = f"{repository_name}.config"

    # Build the spec file
    with open(spec, "w") as f:
        f.write("\n".join(list(map(str, repository_content["paths"]))))

    # Build the config file
    config_content = f"CVMFS_REPOSITORIES={repository_name}\n"
    config_content += f"CVMFS_REPOSITORY_NAME={repository_name}\n"
    config_content += f'CVMFS_SERVER_URL={repository_content["url"]}\n'
    config_content += (
        f'CVMFS_KEYS_DIR={str(Path(repository_content["public_key"]).parent)}\n'
    )
    config_content += "CVMFS_CONFIG_REPOSITORY=cvmfs-config.cern.ch\n"
    config_content += "CVMFS_HTTP_PROXY=DIRECT\n"
    config_content += "CVMFS_CACHE_BASE=/var/lib/cvmfs/shrinkwrap\n"
    config_content += "CVMFS_SHARED_CACHE=no\n"
    config_content += "CVMFS_USER=cvmfs"
    logging.debug(f"{config}:\n{config_content}")

    with open(config, "w") as f:
        f.write(config_content)

    return (spec, config)


# ------------------------------------------------------------------------------


def test(
    apps_dir: str,
    subset_path: str,
    container: str,
    number_cores: int,
    command_outputs: Optional[list[str]] = None,
) -> bool:
    """Check the validity of the inputs

    :type apps_dir: str
    :param apps_dir: directory of applications structured as <apps_dir>/<command>/command.sh
    :type subset_path: str
    :param subset_path: path of the subset of CVMFS
    :type container: str
    :param container: name of the container in which applications will run
    :type number_cores: int
    :param number_cores: number of operations to be done in parallel
    """
    manager = multiprocessing.Manager()
    lock = manager.Lock()  # pylint: disable=no-member
    with ProcessPoolExecutor(max_workers=number_cores) as executor:
        futures = [
            executor.submit(
                test_a_command,
                input_command,
                subset_path,
                container,
                lock,
                command_outputs,
            )
            for input_command in Path(apps_dir).glob("*/command.sh")
        ]
        for future in as_completed(futures):
            if not future.result():
                executor.shutdown(wait=False)
                return False

    return True


def test_a_command(
    input_command: str,
    subset_path: str,
    container: str,
    lock: multiprocessing.Lock,
    command_outputs: Optional[list[str]] = None,
) -> bool:
    """Test an application of interest (multiprocessing)

    :type input_command: str
    :param input_command: directory containing a command and input dependencies
    :type trace_prefix: str
    :param trace_prefix: prefix command to trace the input command
    :type subset_path: str
    :param subset_path: path of the subset of CVMFS
    :type container: str
    :param container: name of the container in which the application will run
    """
    logging.info(f"Start testing {input_command}")

    # Generate the executable
    singularity_executable = Path.cwd().joinpath(f"singularityexec_{uuid.uuid4()}.sh")
    generate_executable(str(singularity_executable), input_command.resolve())

    # Go to the script directory to get the inputs
    current_directory = Path.cwd()
    subset_path_absolute = Path(subset_path).resolve()
    os.chdir(str(input_command.resolve().parent))

    # Set up singularity command
    command = f"singularity exec --cleanenv "
    command += f"--bind {singularity_executable.parent.resolve()} --bind {subset_path_absolute}:/cvmfs "
    command += f"{container} {singularity_executable}"
    logging.debug(f"Command: {command}")

    # Execute it
    result = subprocess.run(
        shlex.split(command), capture_output=(command_outputs != None)
    )
    if result.returncode != 0:
        singularity_executable.unlink()
        os.chdir(str(current_directory))
        logging.error(f"{input_command} testing failed")
        if command_outputs:
            generate_command_outputs(
                command_outputs, result.stdout, result.stderr, lock, input_command
            )
        return False

    # Clean up
    singularity_executable.unlink()
    os.chdir(str(current_directory))
    if command_outputs:
        generate_command_outputs(
            command_outputs, result.stdout, result.stderr, lock, input_command
        )
    logging.info(f"{input_command} successfully tested")
    return True


# ------------------------------------------------------------------------------


def deploy(
    subset_path: str,
    remote_location: str,
    container: Optional[str] = None,
    bootstrap: Optional[str] = None,
    post_command: Optional[str] = None,
    bundle_path: Optional[str] = None,
    command_outputs: Optional[list[str]] = None,
) -> bool:
    """Check the validity of the inputs

    :type subset_path: str
    :param subset_path: path of the subset of CVMFS
    :type remote_location: str
    :param remote_location: remote server address and path to destination
    :type container: str
    :param container: name of the container in which applications will run
    :type bootstrap: str
    :param bootstrap: type of container (e.g. local)
    :type post_command: str
    :param post_command: command to execute once the container is ready
    :type bundle_path: str
    :param bundle_path: container composed of subset_path
    """
    # If container, bootstrap and bundle_path are specified,
    # then we have to generate a bundle to encapsulate the subset
    deploy_content = subset_path
    if container and bootstrap and bundle_path:
        bundle_def_content = generate_cvmfs_container_bundle(
            subset_path, container, bootstrap, post_command
        )
        bundle_def_path = Path.cwd().joinpath(f"bundle_{uuid.uuid4()}.def")
        with open(bundle_def_path, "w") as f:
            f.write(bundle_def_content)

        command = f"singularity build {bundle_path} {bundle_def_path}"
        logging.debug(f"Command: {command}")

        result = subprocess.run(
            shlex.split(command), capture_output=(command_outputs != None)
        )
        if result.returncode != 0:
            bundle_def_path.unlink()
            if command_outputs:
                generate_command_outputs(command_outputs, result.stdout, result.stderr)
            return False

        bundle_def_path.unlink()
        if command_outputs:
            generate_command_outputs(command_outputs, result.stdout, result.stderr)
        deploy_content = bundle_path

    # Deploy to a remote server
    command = f"rsync -a {deploy_content} {remote_location}"
    logging.debug(f"Command: {command}")

    result = subprocess.run(
        shlex.split(command), capture_output=(command_outputs != None)
    )
    if result.returncode != 0:
        if command_outputs:
            generate_command_outputs(command_outputs, result.stdout, result.stderr)
        return False

    if command_outputs:
        generate_command_outputs(command_outputs, result.stdout, result.stderr)
    return True


def generate_cvmfs_container_bundle(
    subset_path: str, container: str, bootstrap: str, post_command: Optional[str] = None
) -> str:
    """Bundle the subset of CVMFS in a container

    :type subset_path: str
    :param subset_path: path of the subset of CVMFS
    :type container: str
    :param container: name of the container in which applications will run
    :type bootstrap: str
    :param bootstrap: type of container
    :type post_command: str
    :param post_command: command to execute once the container is ready
    :return:
    """
    def_file = f"Bootstrap: {bootstrap}\n"
    def_file += f"From: {container}\n\n"
    def_file += f"%files\n{subset_path} /cvmfs\n\n"
    if post_command:
        def_file += f"%post\n{post_command}\n"
    return def_file


# ------------------------------------------------------------------------------


def generate_executable(file_name: str, app_path: str, prefix: str = ""):
    """Generate an executable to execute an application

    :type file_name: str
    :param file_name: executable file name
    :type app_path: str
    :param app_path: path to the application to run
    :type prefix: str
    :param prefix: prefix to the application
    """
    with open(file_name, "w") as f:
        f.write(f"#!/bin/bash\n{prefix}{app_path}")

    file_path = Path(file_name)
    file_path.chmod(0o755)


def generate_command_outputs(
    command_outputs: list[str],
    stdout: str,
    stderr: str,
    lock: Optional[multiprocessing.Lock] = None,
    input_command: str = None,
):
    """Generate a command output file containing details about an execution

    :type command_outputs: list
    :param command_output: name of the files that will contain stdout and stderr
    :type stdout: str
    :param stdout: stdout of a command
    :type stderr: str
    :param stderr: stderr of a command
    :type input_command: str
    :param input_command: directory containing a command and input dependencies
    """
    if lock:
        lock.acquire()
    try:
        stdout_file = Path(command_outputs[0])
        stderr_file = Path(command_outputs[1])

        header = ""
        if input_command:
            header = "==============================\n"
            header += f"{input_command}\n"
            header += "==============================\n"

        with open(stdout_file, "a") as f:
            f.write(header)
            f.write(stdout.decode("utf-8", "backslashreplace"))
        with open(stderr_file, "a") as f:
            f.write(header)
            f.write(stderr.decode("utf-8", "backslashreplace"))
    finally:
        if lock:
            lock.release()
