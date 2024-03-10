from fastapi import FastAPI

from clientpackage import client

app = FastAPI()


@app.get("/movies")
async def get_all_movies():
    return client.get_all_video_information()

@app.get("/movie/{id}")
async def get_movie_information_by_id(id: int):
    return client.get_movie_information_by_id(id)
