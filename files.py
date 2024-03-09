import os


def file_path(file_name: str, folder: str | None) -> str:
    """
    Finds the file path of a file within a folder.

    :param file_name: Name of the file.
    :param folder: Name of the folder. Set as None if file has no folder.
    :return: Absolute Path of the file.
    """

    # if folder is none, file_name will only be the file without the folder
    if folder is not None:
        file_name = folder + os.sep + file_name  # combines names with operating system seperator

    dir_path = os.path.dirname(os.path.realpath(__file__))  # gets the directory of the current script
    return os.path.join(dir_path, file_name)  # constructs the full path to the font file
