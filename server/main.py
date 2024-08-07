import crud
import models
import schemas
import requests
from settings import IMAGE_STORAGE_URL, IMAGE_STORAGE_API_KEY
from utility import make_file_name
from database import SessionLocal, engine
from typing import Annotated
from fastapi import FastAPI, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="MemeCollector")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/memes/")
def create_meme(
        meme: Annotated[schemas.MemeCreate, Depends()],
        image: UploadFile | None = None,
        db: Session = Depends(get_db)
):
    if not image:
        return crud.create_meme(db=db, meme=meme)
    if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=406, detail="Only .jpeg, .jpg, .png files are allowed!")

    try:
        image.filename = make_file_name(image.filename)
        image_content = image.file.read()

        response = requests.post(url=f"{IMAGE_STORAGE_URL}/upload_image/",
                                 files={"image": (image.filename, image_content, image.content_type)},
                                 headers={"Storage-Key": IMAGE_STORAGE_API_KEY})

        if response.status_code == 200:
            image_url = response.json().get("image_url")
            return crud.create_meme(db=db, meme=meme, image_name=image.filename, image_url=image_url)
        else:
            raise HTTPException(status_code=503, detail="Failed to upload file to storage.")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Image storage is currently unavailable.")


@app.get("/memes")
def get_memes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    memes = crud.get_memes(db, skip=skip, limit=limit)
    if len(memes) == 0:
        return {"response": "Didn't find any memes!"}
    return memes


@app.get("/memes/{meme_id}")
def get_meme_by_id(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.get_meme_by_id(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail=f"Meme with ID {meme_id} doesn't exist!")
    return db_meme


@app.put("/memes/{meme_id}")
def update_meme(
        meme_id,
        meme: Annotated[schemas.MemeUpdate, Depends()],
        image: UploadFile | None = None,
        db: Session = Depends(get_db)
):
    db_meme = get_meme_by_id(meme_id, db)

    if not image:
        return crud.update_meme(db=db, meme=meme, meme_id=meme_id)
    if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=406, detail="Only .jpeg, .jpg, .png files are allowed!")

    try:
        image.filename = make_file_name(image.filename)
        image_content = image.file.read()

        response = requests.put(url=f"{IMAGE_STORAGE_URL}/update_image/",
                                data={"old_image_name": db_meme.image_name},
                                files={"new_image": (image.filename, image_content, image.content_type)},
                                headers={"Storage-Key": IMAGE_STORAGE_API_KEY})

        if response.status_code == 200:
            new_image_url = response.json().get("new_image_url")
            return crud.update_meme(db=db, meme=meme, meme_id=meme_id, image_name=image.filename, image_url=new_image_url)
        else:
            raise HTTPException(status_code=503, detail="Failed to upload file to storage.")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Image storage is currently unavailable.")


@app.delete("/memes/{meme_id}")
def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = get_meme_by_id(meme_id, db)
    if not db_meme.image_name:
        crud.delete_meme(db, meme_id=meme_id)
        return JSONResponse(status_code=200,
                            content={"message": f"Meme with ID {meme_id} was successfully deleted!"})

    try:
        response = requests.delete(url=f"{IMAGE_STORAGE_URL}/delete_image/",
                                   data={"image_name": db_meme.image_name},
                                   headers={"Storage-Key": IMAGE_STORAGE_API_KEY})

        if response.status_code == 200:
            crud.delete_meme(db, meme_id=meme_id)
            return JSONResponse(status_code=200,
                                content={"message": f"Meme with ID {meme_id} was successfully deleted!"})
        else:
            raise HTTPException(status_code=503, detail="Failed to delete file from storage.")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Image storage is currently unavailable.")
