import os
from server import crud
from server import models
from server import schemas
from server.utility import make_file_path, delete_file, make_file_name
from server.database import SessionLocal, engine
from image_storage.main import router as image_router
from image_storage.main import upload_image, download_image
from typing import Annotated
from fastapi import FastAPI, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="MemeCollector")
app.include_router(image_router, prefix="/storage")


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

    image_name = make_file_name(image)
    image_path = make_file_path(image_name)
    with open(image_path, "wb") as f:
        content = image.file.read()
        f.write(content)
    result = upload_image(image_name=image_name,
                          image_path=image_path,
                          storage_key=os.getenv("IMAGE_STORAGE_API_KEY"))
    delete_file(image_path)
    if result != 0:
        return crud.create_meme(db=db, meme=meme)
    return crud.create_meme(db=db, meme=meme, image_name=image_name)


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
    if db_meme.image_name:
        download_image(image_name=db_meme.image_name,
                       storage_key=os.getenv("IMAGE_STORAGE_API_KEY")
                       )

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

    image_path = db_meme.image_path
    delete_file(image_path)

    new_image_path = make_file_path(image)
    with open(new_image_path, "wb") as f:
        content = image.file.read()
        f.write(content)
    return crud.update_meme(db=db, meme=meme, meme_id=meme_id, image_path=new_image_path)


@app.delete("/memes/{meme_id}")
def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = get_meme_by_id(meme_id, db)
    image_path = db_meme.image_path
    crud.delete_meme(db, meme_id=meme_id)
    if db_meme.image_path:
        delete_file(image_path)
    return {"response": f"Meme with ID {meme_id} was successfully deleted!"}
