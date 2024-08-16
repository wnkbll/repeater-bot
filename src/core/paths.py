from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

ENV_PATH = ROOT_DIR.joinpath(".env")
IMAGE_DIR = ROOT_DIR.joinpath("data")
LOGGING_DIR = ROOT_DIR.joinpath("logs")
CONFIG_PATH = ROOT_DIR.joinpath("config.json")
SESSION_PATH = ROOT_DIR.joinpath("session/client")
