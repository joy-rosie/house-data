import json
import os
from pathlib import Path

import pytest
import datamate


TEST_PATH_LOG_RAW = "TEST_PATH_LOG_RAW"
TEST_PATH_DATA_RAW = "TEST_PATH_DATA_RAW"
TEST_PATH_KEYS_RAW = "TEST_PATH_KEYS_RAW"
TEST_PATH_LOG = "TEST_PATH_LOG"
TEST_PATH_DATA = "TEST_PATH_DATA"
TEST_PATH_KEYS = "TEST_PATH_KEYS"

KEYS = {
    "name1": "key1",
    "name2": "key2",
}


@pytest.fixture
def path_env(temp_dir: Path):
    path_env = temp_dir.joinpath(".env")
    env_contents = f"""
{datamate.config.PATH_LOG}={TEST_PATH_LOG}
{datamate.config.PATH_DATA}={TEST_PATH_DATA}
{datamate.config.PATH_KEYS}={TEST_PATH_KEYS}
"""
    path_env.write_text(env_contents)
    yield path_env


@pytest.fixture
def adjust_env_variables():
    os.environ[datamate.config.PATH_LOG] = TEST_PATH_LOG_RAW
    os.environ[datamate.config.PATH_DATA] = TEST_PATH_DATA_RAW
    os.environ[datamate.config.PATH_KEYS] = TEST_PATH_KEYS_RAW


@pytest.mark.parametrize(
    "override, expected_path_log, expected_path_data, expected_path_keys",
    [
        (False, TEST_PATH_LOG_RAW, TEST_PATH_DATA_RAW, TEST_PATH_KEYS_RAW),
        (True, TEST_PATH_LOG, TEST_PATH_DATA, TEST_PATH_KEYS),
    ],
)
def test_load_with_override(
    override,
    expected_path_log,
    expected_path_data,
    expected_path_keys,
    path_env,
    adjust_env_variables,
):
    assert datamate.config.load(path_env=path_env, override=override)
    assert os.environ[datamate.config.PATH_LOG] == expected_path_log
    assert os.environ[datamate.config.PATH_DATA] == expected_path_data
    assert os.environ[datamate.config.PATH_KEYS] == expected_path_keys


@pytest.mark.parametrize(
    "path, expected",
    [
        (None, Path(TEST_PATH_LOG_RAW)),
        (Path("test"), Path("test")),
        ("test", Path("test")),
    ],
)
def test_get_path_log(path, adjust_env_variables, expected):
    actual = datamate.config.get_path_log(path=path)
    assert actual == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (None, Path(TEST_PATH_DATA_RAW)),
        (Path("test"), Path("test")),
        ("test", Path("test")),
    ],
)
def test_get_path_data(path, adjust_env_variables, expected):
    actual = datamate.config.get_path_data(path=path)
    assert actual == expected


@pytest.fixture
def path_keys(temp_dir, use_path):
    path_keys = temp_dir.joinpath("keys.json")
    path_keys.write_text(json.dumps(KEYS))
    if use_path:
        yield path_keys
    else:
        os.environ[datamate.config.PATH_KEYS] = str(path_keys)
        yield None


@pytest.mark.parametrize(
    "use_path, expected",
    [
        (True, KEYS),
        (False, KEYS),
    ],
)
def test_get_all_keys(use_path, expected, path_keys):
    actual = datamate.config.get_all_keys(path=path_keys)
    assert actual == expected


@pytest.mark.parametrize(
    "use_path, name, expected",
    [
        (False, "name1", KEYS["name1"]),
        (False, "name2", KEYS["name2"]),
        (True, "name1", KEYS["name1"]),
        (True, "name2", KEYS["name2"]),
    ],
)
def test_get_key_for_name(use_path, name, expected, path_keys):
    actual = datamate.config.get_key_for_name(name=name, path_keys=path_keys)
    assert actual == expected


@pytest.fixture
def path_data(use_path, temp_dir):
    if not use_path:
        os.environ[datamate.config.PATH_DATA] = str(temp_dir)
    yield temp_dir


@pytest.mark.parametrize(
    "use_path, key",
    [
        (True, "key"),
        (False, "key"),
    ],
)
def test_get_path_data_for_key(use_path, key, path_data):
    expected = path_data.joinpath(key)
    if not use_path:
        path_data = None

    actual = datamate.config.get_path_data_for_key(
        key=key,
        path_data=path_data,
    )
    assert actual == expected
    assert actual.exists()
