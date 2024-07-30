import logging
import os
from minio import Minio
# todo boto3
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

UPLOAD_DIR = "./image_storage/temp_uploaded/"
DOWNLOAD_DIR = "./image_storage/temp_downloaded/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

endpoint = os.getenv("MINIO_ENDPOINT")
access_key = os.getenv("MINIO_ACCESS_KEY")
secret_key = os.getenv("MINIO_SECRET_KEY")

try:
    client = Minio(endpoint=endpoint,
                   access_key=access_key,
                   secret_key=secret_key,
                   secure=True)

    bucket_name = "python-bbrsik-fastapipet-bucket"
    if not client.bucket_exists(bucket_name):
        print("No MinIO bucket found.")
        client.make_bucket(bucket_name)
        print("MinIO bucket created.")

    print("Connected to MinIO!")
except:
    print("Failed to connect to MinIO.")
    print("/// SHUTTING DOWN ///")
    exit()
