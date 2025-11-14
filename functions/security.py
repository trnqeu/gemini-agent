import os
from config import WORKING_DIR

def validate_path_within_working_directory(path: str) -> str:
    """
    Validates that a path is within the permitted working directory.
    Returns the absolute path if valid, raises ValueError if not.
    """
    abs_working_dir = os.path.abspath(WORKING_DIR)
    abs_path = os.path.abspath(os.path.join(abs_working_dir, path))
    
    # Security check: prevent directory traversal attacks
    if not abs_path.startswith(abs_working_dir):
        raise ValueError(
            f"Path '{path}' is outside permitted working directory '{WORKING_DIR}'. "
            f"Attempting to access: {abs_path}"
        )
    return abs_path