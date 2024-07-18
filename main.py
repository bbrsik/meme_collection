from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel

app = FastAPI()


class Meme(BaseModel):
    name: str
    description: str | None = None


@app.get("/memes")
async def get_memes_list():
    return {"message": "this page is for getting all the memes"}


@app.get("/memes/{meme_id}")
async def get_meme(meme_id: int):
    return {"meme_id": meme_id}


@app.post("/memes/")
async def post_meme(meme: Meme):
    return meme

