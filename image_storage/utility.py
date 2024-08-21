import datetime
from settings import MINIO_CLIENT, MINIO_BUCKET_NAME
from minio.error import S3Error


def create_temporary_image_url(image_filename: str, expiry_time_minutes=5):
    expiry = datetime.timedelta(minutes=expiry_time_minutes)
    try:
        image_url = MINIO_CLIENT.presigned_get_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=image_filename,
            expires=expiry)
        return image_url
    except S3Error as e:
        print(str(e))
        return None
