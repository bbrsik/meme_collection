from pydantic import BaseModel
import datetime


class MemeBase(BaseModel):
    text: str
    image_path: str | None = None


class MemeCreate(MemeBase):
    pass


class Meme(MemeBase):
    id: int
    upload_date: datetime.datetime

    class Config:
        from_attributes = True
