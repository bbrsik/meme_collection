import schemas
import models
from sqlalchemy.orm import Session


def create_meme(db: Session, meme: schemas.MemeCreate, image_name=None):
    db_meme = models.Meme(
        text=meme.text,
        image_name=image_name
    )
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def update_meme(db: Session, meme: schemas.MemeUpdate, meme_id, image_name=None):

    db_meme = db.get(models.Meme, meme_id)

    if meme.text:
        db_meme.text = meme.text
    if image_name:
        db_meme.image_name = image_name

    db.commit()
    db.refresh(db_meme)
    return db_meme


def delete_meme(db: Session, meme_id: int):
    db_meme = db.get(models.Meme, meme_id)
    db.delete(db_meme)
    db.commit()


def get_memes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meme).offset(skip).limit(limit).all()


def get_meme_by_id(db: Session, meme_id: int):
    return db.get(models.Meme, meme_id)
