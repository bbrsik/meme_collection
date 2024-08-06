import schemas
import models
from sqlalchemy.orm import Session


def create_meme(db: Session, meme: schemas.MemeCreate, image_url=None):
    db_meme = models.Meme(
        text=meme.text,
        image_url=image_url
    )
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def update_meme(db: Session, meme: schemas.MemeUpdate, meme_id, image_url=None):
    db_meme = db.get(models.Meme, meme_id)
    if meme.text:
        db_meme.text = meme.text
    if image_url:
        db_meme.image_url = image_url
    db.commit()
    db.refresh(db_meme)
    return db_meme


def delete_meme(db: Session, meme_id: int):
    db_meme = db.get(models.Meme, meme_id)
    # todo в фильтр передаётся булево значение, однако он работает. как так?
    # db_meme = db.query(models.Meme).filter(models.Meme.id == meme_id).first()
    db.delete(db_meme)
    db.commit()


def get_memes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meme).offset(skip).limit(limit).all()


def get_meme_by_id(db: Session, meme_id: int):
    return db.get(models.Meme, meme_id)
