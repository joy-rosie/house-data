import os
from pathlib import Path

import pytest
import datamate

from .conftest import temp_dir


TEST_PATH_LOG_RAW = 'TEST_PATH_LOG_RAW'
TEST_PATH_DATA_RAW = 'TEST_PATH_DATA_RAW'
TEST_PATH_KEYS_RAW = 'TEST_PATH_KEYS_RAW'
TEST_PATH_LOG = 'TEST_PATH_LOG'
TEST_PATH_DATA = 'TEST_PATH_DATA'
TEST_PATH_KEYS = 'TEST_PATH_KEYS'

@pytest.fixture
def path_env(temp_dir: Path):
    path_env = temp_dir.joinpath('.env')
    env_contents = f'''
{datamate.config.PATH_LOG}={TEST_PATH_LOG}
{datamate.config.PATH_DATA}={TEST_PATH_DATA}
{datamate.config.PATH_KEYS}={TEST_PATH_KEYS}
'''
    path_env.write_text(env_contents)
    yield path_env
    
    
@pytest.fixture
def adjust_env_variables():
    os.environ[datamate.config.PATH_LOG] = TEST_PATH_LOG_RAW
    os.environ[datamate.config.PATH_DATA] = TEST_PATH_DATA_RAW
    os.environ[datamate.config.PATH_KEYS] = TEST_PATH_KEYS_RAW


@pytest.mark.parametrize(
    'override, expected_path_log, expected_path_data, expected_path_keys', 
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
