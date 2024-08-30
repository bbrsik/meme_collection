import os
import json
from minio import Minio, S3Error
from dotenv import load_dotenv, find_dotenv


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
        print("\033[93mNo MinIO bucket found!\033[0m")
        MINIO_CLIENT.make_bucket(MINIO_BUCKET_NAME)
        print("\033[92mMinIO bucket created.\033[0m")

    policy = json.dumps({
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
    })
    MINIO_CLIENT.set_bucket_policy(MINIO_BUCKET_NAME, policy)

except S3Error as e:
    print(str(e))
    print("\033[91mERROR: Failed to connect to MinIO!\033[0m")
    exit()
