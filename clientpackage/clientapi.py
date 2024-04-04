from typing import Dict

from fastapi import FastAPI, Response, Header
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from clientpackage import cacheservice, clientservice

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHUNK_SIZE = 1024 * 1024
VIDEO_EXTENSION = ".mp4"

cache_service = cacheservice.CacheService(60000)


@app.get("/movies")
async def get_all_movies():
    return clientservice.retrieve_all_movies()


@app.get("/movie/{id_}")
async def get_movie_information_by_id(id_: int) -> Dict:
    return clientservice.retrieve_movie_information(id_)


@app.get("/stream/{id_}")
async def stream_movie(id_: int = 0, range: str = Header(None)) -> Response:
    """
    Streams the requested movie using the <id> that has been passed in

    each set of bytes returned are considered partial content as the entire video is not sent back to the client,
    only the amount specified in the range.

    range is part of the header that is automatically sent from the frontend
    :param id_: the id of the video
    :param range: range of bytes to be sent back
    :return: FastAPI.Response object
    """
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    movie_info = await get_movie_information_by_id(id_)
    filesize = movie_info["size"]
    headers = {
        'Content-Range': f'bytes {str(start)}-{str(int(min(end, int(filesize) - 1)))}/{filesize}',
        'Accept-Ranges': 'bytes'
    }
    video_bytes = clientservice.get_video_bytes_for_stream(id_, start, end)
    return Response(video_bytes, status_code=206, headers=headers, media_type="video/mp4")


@app.post("/upload")
async def upload_movie(title: str, filename: str):
    response = clientservice.upload(title, filename)

    return response.ack


class User(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user: str
    token: int


@app.post("/user/create")
async def create_account(user: User):
    username = user.username
    password = user.password

    created = clientservice.create_user(username, password)
    user_id = created.userId
    if created.can_log_in:
        return JSONResponse(jsonable_encoder(UserResponse(user=username, token=user_id)))
    return JSONResponse(jsonable_encoder(UserResponse(user=username, token=user_id)), status_code=400)


@app.post("/user/login")
async def login(user: User):
    username = user.username
    password = user.password

    created = clientservice.login(username, password)
    user_id = created.userId

    if created.can_log_in:
        return JSONResponse(jsonable_encoder(UserResponse(user=username, token=user_id)), status_code=200)
    return JSONResponse(jsonable_encoder(UserResponse(user="", token=-1)), status_code=400)


class ValidationResponse(BaseModel):
    is_validated: bool


@app.get("/user/authenticated")
async def check_authentication(token: int, username: str):
    authentication_response = clientservice.is_authenticated(token, username)
    if authentication_response:
        return JSONResponse(jsonable_encoder(ValidationResponse(is_validated=True)))
    return JSONResponse(jsonable_encoder(ValidationResponse(is_validated=False)), status_code=401)
