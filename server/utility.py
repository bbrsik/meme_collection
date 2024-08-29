import os
from settings import MINIO_URL, MINIO_BUCKET_NAME
from secrets import token_hex


def make_file_name(filename):
    file_extension = filename.split(".").pop()
    file_name = token_hex(10)
    new_filename = f"{file_name}.{file_extension}"
    return new_filename


def create_image_url(image_filename: str):
    image_url = f"{MINIO_URL}/{MINIO_BUCKET_NAME}/{image_filename}"
    return image_url


def make_downloaded_file_name(filename):
    ext = os.path.splitext(filename)[1]
    downloaded_filename = "downloaded_file_" + token_hex(2) + ext
    return downloaded_filename
