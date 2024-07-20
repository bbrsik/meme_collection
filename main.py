import crud
import models
import schemas
from utility import make_file_path
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="MemeCollector")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/memes/", response_model=schemas.Meme)
def create_meme(
        meme: Annotated[schemas.MemeCreate, Depends()],
        image: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=406, detail="Only .jpeg, .jpg, .png files are allowed")

    image_path = make_file_path(image)

    with open(image_path, "wb") as f:
        content = image.file.read()
        f.write(content)
    return crud.create_meme(db=db, meme=meme, image_path=image_path)


@app.get("/memes")
def get_memes(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    memes = crud.get_memes(db, skip=skip, limit=limit)
    return memes


@app.get("/memes/{meme_id}")
def get_meme_by_id(
        meme_id: int, db: Session = Depends(get_db)
):
    db_meme = crud.get_meme_by_id(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme
