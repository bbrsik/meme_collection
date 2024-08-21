import os
import json
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
MINIO_URL = os.getenv("MINIO_URL")
IMAGE_STORAGE_API_KEY = os.getenv("IMAGE_STORAGE_API_KEY")

try:
    MINIO_CLIENT = Minio(endpoint=MINIO_ENDPOINT,
                         access_key=MINIO_ACCESS_KEY,
                         secret_key=MINIO_SECRET_KEY,
                         secure=False)

    if not MINIO_CLIENT.bucket_exists(MINIO_BUCKET_NAME):
        print("No MinIO bucket found.")
        MINIO_CLIENT.make_bucket(MINIO_BUCKET_NAME)
        print("MinIO bucket created.")

    # todo delete if not needed
    # not sure if public policy is actually required
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "s3:GetObject"
                ],
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "*"
                    ]
                },
                "Resource": [
                    f"arn:aws:s3:::{MINIO_BUCKET_NAME}/*"
                ],
                "Sid": ""
            }
        ]
    }

    if not policy == MINIO_CLIENT.get_bucket_policy(MINIO_BUCKET_NAME):
        MINIO_CLIENT.set_bucket_policy(MINIO_BUCKET_NAME, json.dumps(policy))
        print("Changed MinIO bucket policy.")

except S3Error as e:
    print("Failed to connect to MinIO")
    print(str(e))
    print("Failed to connect to MinIO")
