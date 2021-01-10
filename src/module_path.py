import os.path
import pathlib

def get_project_path(argv0:str) -> pathlib.Path:
    program_path:pathlib.Path = pathlib.Path(argv0)
    if program_path.suffix == '.py':
        return program_path.parent.parent
    elif program_path.suffix == '.exe':
        return program_path.parent