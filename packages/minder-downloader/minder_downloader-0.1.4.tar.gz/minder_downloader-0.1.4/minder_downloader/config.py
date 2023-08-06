from .utils import path_exists, write_yaml,load_yaml
from .update import get_token
from pathlib import Path
import os


def check_config():
    """Check if a configuration file exists, and create/update it with required information.

    This function checks if a YAML configuration file named 'info.yaml' exists in the same directory as this script. If the file doesn't exist, it creates it with default headers and server information, and sets the TOKEN value to None. If the file exists, it loads its contents, retrieves the TOKEN value, and updates it with a new token if the value is None. It then writes the updated information back to the file.

    Returns:
    None
    """
    TOKEN = os.environ.get('RESEARCH_PORTAL_TOKEN_PATH') # check if token is set at the environment level
    root = os.environ.get('MINDER_DOWNLOADER_HOME', Path(__file__).parent)
    info_path = f'{root}{os.sep}info.yaml'
    if not path_exists(info_path):
        tmp = {'headers':{ 'Accept': 'text/plain',
                        'Connection': 'keep-alive',
                        'Content-type': 'application/json'},  
                'server': 'https://research.minder.care/api'}
    else:
        tmp = load_yaml(info_path)
        TOKEN = tmp['token']
    if  TOKEN is None: 
        TOKEN = get_token()
    tmp['token'] = TOKEN
    write_yaml(info_path,tmp)
    

    

