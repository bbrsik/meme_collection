import os
import logging
# todo import boto3
from minio import Minio
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

UPLOAD_DIR = "./temp_uploaded/"
DOWNLOAD_DIR = "./temp_downloaded/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket_name = os.getenv("MINIO_BUCKET_NAME")
endpoint = os.getenv("MINIO_ENDPOINT")
access_key = os.getenv("MINIO_ACCESS_KEY")
secret_key = os.getenv("MINIO_SECRET_KEY")
print(bucket_name, endpoint, access_key, secret_key)

client = Minio(endpoint=endpoint,
               access_key=access_key,
               secret_key=secret_key,
               secure=False)

if not client.bucket_exists(bucket_name):
    print("No MinIO bucket found.")
    client.make_bucket(bucket_name)
    print("MinIO bucket created.")

print("Connected to MinIO!")

