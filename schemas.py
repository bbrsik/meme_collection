from pydantic import BaseModel, FilePath
import datetime


class MemeBase(BaseModel):
    text: str


class MemeCreate(MemeBase):
    pass


class Meme(MemeBase):
    id: int
    upload_date: datetime.datetime

    class Config:
        from_attributes = True
