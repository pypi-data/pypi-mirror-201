import os
from pathlib import Path


def get_project_dir() -> str:
    # Look for __project_root__.py to get the project dir
    files = [str(p) for p in list(Path(os.getcwd()).glob("**/__project_root__.py"))]
    return files[0].replace("/__project_root__.py", "")
