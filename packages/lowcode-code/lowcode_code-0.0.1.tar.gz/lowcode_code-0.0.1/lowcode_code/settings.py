from dynaconf import Dynaconf
from pathlib import Path
from dotenv import load_dotenv
import logging.config

load_dotenv(verbose=True)

BASE_DIR = Path(__file__).parent

settings = Dynaconf(
    settings_files=[BASE_DIR / 'settings.yaml'],
    environments=True,
    BASE_DIR=BASE_DIR
)

logging.config.dictConfig(settings.get('log', {}))
