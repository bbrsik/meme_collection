from sqlalchemy import Column, Integer, String, DateTime
from server.database import Base
import datetime


class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True)

    text = Column(String, index=True)
    image_path = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.datetime.now)
