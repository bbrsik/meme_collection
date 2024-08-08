import os
from secrets import token_hex
from settings import UPLOAD_DIR


def make_file_name(filename):
    file_extension = filename.split(".").pop()
    file_name = token_hex(10)
    new_filename = f"{file_name}.{file_extension}"
    return new_filename


# obsolete
def make_file_path(full_file_name):
    file_path = f"{UPLOAD_DIR}/{full_file_name}"
    return file_path


# obsolete
def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        return 0
    return -1
