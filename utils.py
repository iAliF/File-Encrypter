import os
from typing import Tuple


def check_path(path: str) -> Tuple[bool, bool]:
    """
    Check whether a path exists and is a directory or not
    :param path: Path to check
    :return: Two bools indicating whether a path exists and is a directory or not
    """
    if os.path.exists(path):
        return True, os.path.isdir(path)

    return False, False
