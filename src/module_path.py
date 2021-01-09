import os.path
import pathlib

def get_project_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent.parent