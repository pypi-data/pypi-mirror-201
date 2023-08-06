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
from pathlib import Path
import pytest

from subcvmfs.steps import (
    generate_trace_prefix,
    process_user_paths,
    get_subset_paths,
    process_subset_paths,
    setup_config_spec_files,
    generate_cvmfs_container_bundle,
    generate_executable,
)


@pytest.mark.parametrize(
    "repositories, http_proxy, namelist, envlist, expected",
    [
        (
            {
                "repo1": {"url": "url1", "public_key": "pubkey1"},
                "repo2": {"url": "url2", "public_key": "pubkey2"},
            },
            "DIRECT",
            "namelist.txt",
            "envlist.txt",
            "prefix1.sh",
        )
    ],
)
def test_generate_trace_prefix(repositories, http_proxy, namelist, envlist, expected):
    result = generate_trace_prefix(repositories, http_proxy, namelist, envlist)

    with open(f"tests/trace_prefix/{expected}") as f:
        expected_content = f.read()
    assert result.strip() == expected_content.strip()


# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "namelists, expected",
    [
        (
            ["tests/cvmfs/*"],
            [
                "tests/cvmfs/repo1/lib/file1.sl.txt",
                "tests/cvmfs/repo1/lib/file1.txt",
                "tests/cvmfs/repo1/lib/bin/file2.txt",
                "tests/cvmfs/repo1/bin/file2.txt",
                "tests/cvmfs/repo2/file3.txt",
            ],
        )
    ],
)
def test_process_user_paths(namelists, expected):
    namelists_abs = []
    for path in namelists:
        namelists_abs.append(str(Path.cwd().joinpath(path)))

    process_user_paths(namelists_abs)

    expected_objects = []
    for path in expected:
        expected_objects.append(str(Path.cwd().joinpath(path)))

    assert namelists_abs.sort() == expected_objects.sort()


@pytest.mark.parametrize(
    "namelists, expected",
    [
        (
            [
                "tests/cvmfs/repo1/lib/file1.sl.txt",
                "tests/cvmfs/repo1/lib/bin/file2.txt",
                "tests/cvmfs/repo3/donotexist.txt",
            ],
            [
                "tests/cvmfs/repo1/lib/file1.sl.txt",
                "tests/cvmfs/repo1/lib/file1.txt",
                "tests/cvmfs/repo1/lib/bin/file2.txt",
                "tests/cvmfs/repo1/bin/file2.txt",
            ],
        )
    ],
)
def test_get_subset_paths(namelists, expected):
    namelists_abs = []
    for path in namelists:
        namelists_abs.append(str(Path.cwd().joinpath(path)))

    result = get_subset_paths(namelists_abs)

    expected_objects = set()
    for path in expected:
        expected_objects.add(Path.cwd().joinpath(path))

    assert result == expected_objects


@pytest.mark.parametrize(
    "repositories, paths, expected",
    [
        (
            {
                "repo1": {"url": "url1", "pubkey": "pubkey1"},
                "repo2": {"url": "url2", "pubkey": "pubkey2"},
            },
            [
                "/cvmfs/repo2/file3.txt",
                "/cvmfs/repo1/lib/file1.txt",
                "/cvmfs/repo1/lib/file2.sl.txt",
                "/cvmfs/repo1/bin/*",
                "/cvmfs/repo3/donotexist.txt",
            ],
            {
                "repo1": {
                    "paths": [
                        Path("/lib/file1.txt"),
                        Path("/lib/file2.sl.txt"),
                        Path("/bin/*"),
                    ]
                },
                "repo2": {"paths": [Path("/file3.txt")]},
            },
        )
    ],
)
def test_process_subset_paths(repositories, paths, expected):
    paths_objects = []
    for path in paths:
        paths_objects.append(Path(path))

    process_subset_paths(repositories, paths_objects)
    assert repositories.keys() == expected.keys()
    for key, value in repositories.items():
        assert value["paths"] == expected[key]["paths"]


@pytest.mark.parametrize(
    "repository_name, repository_content, expected_config, expected_spec",
    [
        (
            "repo1",
            {
                "url": "url1",
                "public_key": "/path/to/pubkey",
                "paths": [Path("/lib/file1.txt"), Path("/bin/file2.txt")],
            },
            "CVMFS_REPOSITORIES=repo1",
            "/lib/file1.txt\n/bin/file2.txt",
        )
    ],
)
def test_setup_config_spec_files(
    repository_name, repository_content, expected_config, expected_spec
):

    spec, config = setup_config_spec_files(repository_name, repository_content)

    assert Path(config).exists()
    assert Path(spec).exists()

    with open(config) as f:
        config_content = f.read()
    with open(spec) as f:
        spec_content = f.read()

    assert expected_config in config_content
    assert spec_content == expected_spec

    Path(config).unlink()
    Path(spec).unlink()


# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "subset_path, container, bootstrap, post_command, expected",
    [
        (
            "subset_cvmfs",
            "/cvmfs/cernvm-prod.cern.ch/cvm4",
            "local",
            "source .bashrc",
            "tests/def_files/bundle1.def",
        )
    ],
)
def test_generate_cvmfs_container_bundle(
    subset_path, container, bootstrap, post_command, expected
):
    bundle_content = generate_cvmfs_container_bundle(
        subset_path, container, bootstrap, post_command
    )

    with open(expected) as f:
        expected_content = f.read()

    assert bundle_content == expected_content


# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "file_name, app_path, prefix, expected",
    [
        (
            "executable.sh",
            "tests/inputs/exec.sh",
            "parrot_run ",
            "#!/bin/bash\nparrot_run tests/inputs/exec.sh",
        )
    ],
)
def test_generate_executable(file_name, app_path, prefix, expected):
    generate_executable(file_name, app_path, prefix)

    generated_file = Path(file_name)
    assert generated_file.exists()

    with open(generated_file) as f:
        content = f.read()

    assert content == expected

    mode_before = generated_file.stat().st_mode
    generated_file.chmod(0o755)
    mode_after = generated_file.stat().st_mode
    assert mode_before == mode_after

    generated_file.unlink()
