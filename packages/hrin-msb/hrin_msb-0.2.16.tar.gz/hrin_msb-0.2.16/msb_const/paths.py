from pathlib import Path

from . import names as const_names

"""
DEFAULT PATHS
"""

# path list under root directory
BASE_DIR_PATH = Path(Path.cwd().__str__().split(const_names.RESOURCES_DIR_NAME)[0])
APP_DIR_PATH = BASE_DIR_PATH.joinpath(const_names.APP_DIR_NAME)
WRITABLE_DIR_PATH = BASE_DIR_PATH.joinpath(const_names.WRITABLE_DIR_NAME)
RESOURCE_DIR_PATH = BASE_DIR_PATH.joinpath(const_names.RESOURCES_DIR_NAME)

PROD_ENV_FILE_PATH = BASE_DIR_PATH.joinpath(const_names.PROD_ENV_FILE_NAME)
DEV_ENV_FILE_PATH = BASE_DIR_PATH.joinpath(const_names.DEV_ENV_FILE_NAME)

# path list under writable directory
LOGS_DIR_PATH = WRITABLE_DIR_PATH.joinpath(const_names.LOGS_DIR_NAME)

# path list under resources directory
FIXTURES_DIR_PATH = RESOURCE_DIR_PATH.joinpath(const_names.FIXTURES_DIR_NAME)
RESOURCE_CONFIG_DIR_PATH = RESOURCE_DIR_PATH.joinpath(const_names.RESOURCE_CONFIG_DIR_NAME)
SETUP_SCRIPTS_DIR_PATH = RESOURCE_DIR_PATH.joinpath(const_names.SETUP_SCRIPTS_DIR_NAME)
TEST_DATA_DIR_PATH = RESOURCE_DIR_PATH.joinpath(const_names.TEST_DATA_DIR_NAME)

# path list under fixtures directory
BASE_FIXTURES_DIR_PATH = FIXTURES_DIR_PATH.joinpath(const_names.DEFAULT_FIXTURE_DIR_NAME),
PROD_FIXTURES_DIR_PATH = FIXTURES_DIR_PATH.joinpath(const_names.PROD_FIXTURE_DIR_NAME),
TEST_FIXTURES_DIR_PATH = FIXTURES_DIR_PATH.joinpath(const_names.TEST_FIXTURE_DIR_NAME),

# compiled constants
SYS_PATH_LIST = [
	BASE_DIR_PATH.__str__(), APP_DIR_PATH.__str__(),
	RESOURCE_DIR_PATH.__str__(), WRITABLE_DIR_PATH.__str__()
]

FIXTURE_DIRS_LIST = [BASE_FIXTURES_DIR_PATH, PROD_FIXTURES_DIR_PATH, TEST_FIXTURES_DIR_PATH]
