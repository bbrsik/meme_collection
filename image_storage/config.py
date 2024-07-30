from minio import Minio
import os

UPLOAD_DIR = "./image_storage/temp_uploaded/"
DOWNLOAD_DIR = "./image_storage/temp_downloaded/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

endpoint = os.getenv("MINIO_ENDPOINT")
access_key = os.getenv("MINIO_ACCESS_KEY")
secret_key = os.getenv("MINIO_SECRET_KEY")

try:
    client = Minio(endpoint=f"{endpoint}",
                   access_key=f"{access_key}",
                   secret_key=f"{secret_key}",
                   secure=True)

    bucket_name = "python-bbrsik-fastapipet-bucket"
    if not client.bucket_exists(bucket_name):
        print("No MinIO bucket found.")
        client.make_bucket(bucket_name)
        print("MinIO bucket created.")

    print("Connected to MinIO!")
except:
    print("Failed to connect to MinIO.")
    print('/// SHUTTING DOWN ///')
    exit()
