from pydantic import BaseModel, FilePath
import datetime


class MemeBase(BaseModel):
    text: str


class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    text: str


class MemeDelete(MemeBase):
    pass


class Meme(MemeBase):
    id: int
    image_path: str
    upload_date: datetime.datetime

    class Config:
        from_attributes = True
