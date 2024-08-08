import os
import logging
from minio import Minio, S3Error
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger(__name__)
# todo настроить логи

if find_dotenv():
    load_dotenv()
else:
    print('No .env file found.')
    print('Please check the .env.example file and create the .env file.')
    print('/// SHUTTING DOWN ///')
    exit()

MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

try:
    client = Minio(endpoint=MINIO_ENDPOINT,
                   access_key=MINIO_ACCESS_KEY,
                   secret_key=MINIO_SECRET_KEY,
                   secure=False)

    if not client.bucket_exists(MINIO_BUCKET_NAME):
        print("No MinIO bucket found.")
        client.make_bucket(MINIO_BUCKET_NAME)
        print("MinIO bucket created.")

except S3Error as e:
    print("Failed to connect to MinIO")
    print(str(e))
    print("Failed to connect to MinIO")
