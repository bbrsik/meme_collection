import os
from fastapi import APIRouter, HTTPException
from image_storage.config import client, bucket_name
from image_storage.config import DOWNLOAD_DIR

# todo на другой порт
router = APIRouter()


# todo сделать генерацию ключа хранилища при запуске приложения
# todo или генерировать новый ключ на каждый вызов метода
@router.post("/upload_image/")
def upload_image(image_name=None, image_path=None, storage_key=None):
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")
    if not client.bucket_exists(bucket_name=bucket_name):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")
    try:
        result = client.fput_object(bucket_name=bucket_name, object_name=image_name, file_path=image_path)
    except:
        raise HTTPException(status_code=503, detail="Failed to upload image to storage.")
    return {"detail": "success"}


@router.get("/download_image/")
def download_image(image_name=None, storage_key=None):
    download_path = DOWNLOAD_DIR + image_name
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")
    if not client.bucket_exists(bucket_name=bucket_name):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")
    try:
        result = client.fget_object(bucket_name=bucket_name, object_name=image_name, file_path=download_path)
    except:
        raise HTTPException(status_code=503, detail="Failed to download image from storage.")
    return {"detail": "success"}


@router.delete("/delete_image/")
def delete_image(image_name=None, storage_key=None):
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")
    if not client.bucket_exists(bucket_name=bucket_name):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")
    try:
        client.remove_object(bucket_name=bucket_name, object_name=image_name)
    except:
        raise HTTPException(status_code=503, detail="Failed to delete image from storage.")
    return {"detail": "success"}


@router.get("/list_images/")
def list_images():
    objects = client.list_objects(bucket_name=bucket_name)
    result = []
    for obj in objects:
        result.append(obj)
    return result

