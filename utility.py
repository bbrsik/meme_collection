import os
from secrets import token_hex
from settings import UPLOAD_DIR


def make_file_path(file):
    file_extension = file.filename.split(".").pop()
    file_name = token_hex(10)
    file_path = f"{UPLOAD_DIR}/{file_name}.{file_extension}"
    return file_path


def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        return 0
    return -1
