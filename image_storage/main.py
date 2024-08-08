import os
import requests
from settings import client, bucket_name
from settings import DOWNLOAD_DIR
from fastapi import FastAPI, HTTPException


app = FastAPI(title="ImageStorage")


@app.post("/upload_image/")
def upload_image(request, storage_key=None):
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")
    if not client.bucket_exists(bucket_name=bucket_name):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")
    try:
        request.POST.get()
        result = client.put_object(bucket_name=bucket_name, object_name=image.filename, data=image.file)
    except:
        raise HTTPException(status_code=503, detail="Failed to upload image to storage.")
    return {"detail": "success"}


@app.get("/download_image/")
def download_image(request, storage_key=None):
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


@app.delete("/delete_image/")
def delete_image(request, storage_key=None):
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")
    if not client.bucket_exists(bucket_name=bucket_name):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")
    try:
        client.remove_object(bucket_name=bucket_name, object_name=image_name)
    except:
        raise HTTPException(status_code=503, detail="Failed to delete image from storage.")
    return {"detail": "success"}
