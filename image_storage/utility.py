import datetime
from settings import MINIO_CLIENT, MINIO_BUCKET_NAME, MINIO_URL
from minio.error import S3Error


def create_image_url(image_filename):
    image_url = f"{MINIO_URL}/{MINIO_BUCKET_NAME}/{image_filename}"
    return image_url


def create_temporary_image_url(image_filename, expiry_time: int):
    expiry = datetime.timedelta(hours=1)
    try:
        image_url = MINIO_CLIENT.presigned_get_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=image_filename,
            expires=expiry)
        return image_url
    except S3Error as e:
        return None
