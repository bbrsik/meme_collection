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


def delete_meme(db: Session, meme: schemas.MemeCreate, image_path=None):
    pass


def get_memes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meme).offset(skip).limit(limit).all()


def get_meme_by_id(db: Session, meme_id: int):
    return db.query(models.Meme).filter(models.Meme.id == meme_id).first()
