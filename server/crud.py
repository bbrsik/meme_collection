from sqlalchemy.orm import Session
import models
import schemas


def create_meme(db: Session, meme: schemas.MemeCreate, image_path=None):
    db_meme = models.Meme(
        text=meme.text,
        image_path=image_path
    )
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def update_meme(db: Session, meme: schemas.MemeUpdate, meme_id, image_path=None):
    db_meme = db.get(models.Meme, meme_id)
    if meme.text:
        db_meme.text = meme.text
    if image_path:
        db_meme.image_path = image_path
    db.commit()
    db.refresh(db_meme)
    return db_meme


def delete_meme(db: Session, meme_id: int):
    db_meme = db.get(models.Meme, meme_id)
    # todo в фильтр передаётся булево, но работает. как?
    # db_meme = db.query(models.Meme).filter(models.Meme.id == meme_id).first()
    db.delete(db_meme)
    db.commit()


def get_memes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meme).offset(skip).limit(limit).all()


def get_meme_by_id(db: Session, meme_id: int):
    return db.get(models.Meme, meme_id)
