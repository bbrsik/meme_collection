import datetime
from database import Base
from sqlalchemy import Column, Integer, String


class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True)
    image_name = Column(String, index=True)
    upload_date = Column(String, default=datetime.datetime.now)
