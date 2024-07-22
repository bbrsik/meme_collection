from pydantic import BaseModel, FilePath
import datetime


class MemeBase(BaseModel):
    text: str


class Meme(MemeBase):
    id: int
    image_path: str
    upload_date: datetime.datetime

    class Config:
        from_attributes = True


class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    pass
