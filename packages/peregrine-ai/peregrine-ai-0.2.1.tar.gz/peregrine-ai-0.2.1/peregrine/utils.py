import typer
import dotenv
import os
from pathlib import Path
import openai

class models:
    """
    Default = GPT_3P5_TURBO
    """
    GPT_3P5_TURBO = "gpt-3.5-turbo"
    TEXT_DAVINCI_003 = "text-davinci-003"
    CODE_DAVINCI_002 = "code-davinci-002"
    TEXT_ADA_001 = "text-ada-001"

    MAPPING = {1: GPT_3P5_TURBO, 2: TEXT_DAVINCI_003, 3: CODE_DAVINCI_002, 4: TEXT_ADA_001}


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


env_path = Path.home().joinpath(".peregrine")
env_file_path = env_path.joinpath(".env")

def make_env():
    Path.mkdir(env_path, exist_ok=True)
    Path.touch(env_file_path, exist_ok=True)

    dotenv.load_dotenv(dotenv_path=env_file_path)

    saved_key = os.getenv("OPENAI_API_KEY")
    saved_model = os.getenv("MODEL")

    if not saved_model:
        set_model(1)


def set_key(key) -> bool:

    dotenv.set_key(env_file_path, "OPENAI_API_KEY", key)
    get_key()
    
    return True


def get_key() -> str:
    
    key = os.getenv("OPENAI_API_KEY")

    if key:
        openai.api_key = key
    
    return key


def get_model():
    model = os.getenv("MODEL")
    return model
 
 
def set_model(model: int):
    model_name = models.MAPPING[model]
    dotenv.set_key(env_file_path, "MODEL", model_name)