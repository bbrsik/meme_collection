import datetime
from pydantic import BaseModel
from fastapi import UploadFile

class MemeBase(BaseModel):
    text: str | None = None


class Meme(MemeBase):
    id: int
    image_name: str | None = None
    upload_date: datetime.datetime

    class Config:
        from_attributes = True


class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    pass
