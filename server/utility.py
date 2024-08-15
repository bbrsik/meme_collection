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
