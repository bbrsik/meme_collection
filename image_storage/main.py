import os
from utility import create_image_url
from settings import MINIO_CLIENT, MINIO_BUCKET_NAME
from minio import S3Error
from fastapi import FastAPI, HTTPException, UploadFile, Request, Form
from fastapi.responses import JSONResponse
from io import BytesIO

app = FastAPI(title="ImageStorage")


@app.post("/upload_image/")
def upload_image(request: Request,
                 image: UploadFile):

    storage_key = request.headers.get("Storage-Key")
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")

    if not MINIO_CLIENT.bucket_exists(bucket_name=MINIO_BUCKET_NAME):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")

    try:
        MINIO_CLIENT.put_object(bucket_name=MINIO_BUCKET_NAME,
                                object_name=image.filename,
                                data=BytesIO(image.file.read()),
                                length=-1,
                                part_size=10 * 1024 * 1024,
                                content_type=image.content_type)

        image_url = create_image_url(image.filename)

    except S3Error as e:
        raise HTTPException(status_code=503, detail=str(e))

    return JSONResponse(status_code=200, content={"image_url": image_url})


@app.delete("/delete_image/")
def delete_image(request: Request,
                 image_name: str = Form(...)):

    storage_key = request.headers.get("Storage-Key")
    if not storage_key == os.getenv("IMAGE_STORAGE_API_KEY"):
        raise HTTPException(status_code=403, detail="Access denied.")

    if not MINIO_CLIENT.bucket_exists(bucket_name=MINIO_BUCKET_NAME):
        raise HTTPException(status_code=503, detail="Bucket does not exist.")

    try:
        MINIO_CLIENT.remove_object(bucket_name=MINIO_BUCKET_NAME, object_name=image_name)
    except S3Error as e:
        raise HTTPException(status_code=503, detail=str(e))

    return JSONResponse(status_code=200, content={"message": f"Object '{image_name}' was successfully deleted!"})
