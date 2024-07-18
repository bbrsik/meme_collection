import crud
import models
import schemas
import os
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "uploaded_memes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/memes/", response_model=schemas.Meme)
def create_meme(
        meme: Annotated[schemas.MemeCreate, Depends()],
        db: Session = Depends(get_db)):
    return crud.create_meme(db=db, meme=meme)


@app.get("/memes")
def get_memes(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    memes = crud.get_memes(db, skip=skip, limit=limit)
    return memes
