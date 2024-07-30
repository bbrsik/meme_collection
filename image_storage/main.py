from fastapi import APIRouter, HTTPException
from minio import Minio
import os

router = APIRouter()

endpoint = os.getenv("MINIO_ENDPOINT")
access_key = os.getenv("MINIO_ACCESS_KEY")
secret_key = os.getenv("MINIO_SECRET_KEY")

print("Connecting to MinIO...")

client = Minio(endpoint=f"{endpoint}",
               access_key=f"{access_key}",
               secret_key=f"{secret_key}",
               secure=True)


# todo сделать генерацию ключа хранилища при запуске приложения
# todo или генерировать новый ключ на каждый вызов метода
@router.post("/upload_image/")
def upload_image(storage_key=None):
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")

    return {"message": "ready to upload"}


@router.get("/download_image/")
def download_image(storage_key=None):
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")

    return {"message": "ready to download"}
