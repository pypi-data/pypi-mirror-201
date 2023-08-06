import os
from pathlib import Path

def get_project_dir() -> str:
    # Look for __project_root__.py to get the project dir
    return Path(os.getcwd()).glob('**/__project_root__.py', recursive=True)