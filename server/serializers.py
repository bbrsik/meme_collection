from settings import SERVER_URL


def serialize_meme(db_meme):
    serialized_meme = {
        "id": db_meme.id,
        "text": db_meme.text,
        "upload_date": db_meme.upload_date
    }
    if db_meme.image_name:
        serialized_meme["image_url"] = f"{SERVER_URL}/memes/{db_meme.id}/image"
    return serialized_meme


def serialize_memes(db_memes: list):
    # todo list comp
    serialized_memes = []
    for db_meme in db_memes:
        serialized_memes.append(serialize_meme(db_meme))
    return serialized_memes
