import os
import requests
from settings import client, MINIO_BUCKET_NAME
from minio import S3Error
from fastapi import FastAPI, HTTPException, UploadFile, Request, Header
from io import BytesIO

app = FastAPI(title="ImageStorage")


@app.post("/upload_image/")
def upload_image(image: UploadFile,
                 request: Request):

    storage_key = request.headers.get("Storage-Key")
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")

    if not client.bucket_exists(bucket_name=MINIO_BUCKET_NAME):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")

    try:
        client.put_object(bucket_name=MINIO_BUCKET_NAME,
                          object_name=image.filename,
                          data=BytesIO(image.file.read()),
                          length=-1,
                          part_size=10 * 1024 * 1024,
                          content_type=image.content_type)
    except S3Error as e:
        raise HTTPException(status_code=503, detail=str(e))

    return {"detail": "success"}


@app.get("/download_image/")
def download_image(request, storage_key=None):
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")
    if not client.bucket_exists(bucket_name=MINIO_BUCKET_NAME):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")
    try:
        result = client.fget_object(bucket_name=MINIO_BUCKET_NAME, object_name=image_name, file_path=download_path)
    except:
        raise HTTPException(status_code=503, detail="Failed to download image from storage.")
    return {"detail": "success"}


@app.delete("/delete_image/")
def delete_image(storage_key=None):
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")
    if not client.bucket_exists(bucket_name=MINIO_BUCKET_NAME):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")
    try:
        client.remove_object(bucket_name=MINIO_BUCKET_NAME, object_name=image_name)
    except:
        raise HTTPException(status_code=503, detail="Failed to delete image from storage.")
    return {"detail": "success"}
