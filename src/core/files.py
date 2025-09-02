import os


def path(path: str) -> str:
    """
    Finds the file path of a file within a folder.

    :param path: Path of the file relative to the root.
    :return: Absolute Path of the file.
    """

    this_file = os.path.realpath(__file__)  # gets the directory of the current script
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))  # strips three levels of directories to get the root

    return os.path.join(root_path, path)  # combines the root path with the relative path
