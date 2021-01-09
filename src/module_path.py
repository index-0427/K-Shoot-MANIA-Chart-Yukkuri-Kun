import os.path
import pathlib

def get_project_path(argv0) -> pathlib.Path:
    return pathlib.Path(argv0).parent.parent