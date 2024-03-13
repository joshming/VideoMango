import os
from pathlib import Path
from typing import Dict, Any

import google
import grpc
from fastapi import FastAPI, Response, Header
from fastapi.middleware.cors import CORSMiddleware

from proto import server_pb2_grpc, server_pb2

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


@app.get("/movies")
async def get_all_movies():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response_iterator = stub.getAllVideos(google.protobuf.empty_pb2.Empty())
        videos = []
        for video in response_iterator:
            videos.append({"id": video.id, "title:": video.title})
        return videos


@app.get("/movie/{id}")
async def get_movie_information_by_id(id: int) -> Dict:
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response = stub.getVideoInformation(server_pb2.VideoRequest(videoId=id))
        return {"id": response.id, "title": response.title, "size": response.size}


@app.get("/stream/{id_}")
async def stream_movie(id_: int = 0, range: str = Header(None)):
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    filesize = (await get_movie_information_by_id(id_))["size"]
    headers = {
        'Content-Range': f'bytes {str(start)}-{str(int(min(end, int(filesize))))}/{filesize}',
        'Accept-Ranges': 'bytes'
    }
    totalChunks = b''
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response_iterator = stub.StreamVideo(server_pb2.VideoRequest(videoId=id_))
        for response in response_iterator:
            totalChunks += response.chunk
    return Response(totalChunks[start:end + 1], status_code=206, headers=headers, media_type="video/mp4")


def create_upload_iterator(filename: str):
    filename = filename + VIDEO_EXTENSION
    with open(filename, 'rb') as compressed_file:
        while True:
            chunk = compressed_file.read(CHUNK_SIZE)
            if len(chunk) == 0:
                os.remove(filename)
                return
            yield server_pb2.Chunk(chunk=chunk)


@app.post("/upload")
async def upload_movie(title: str, filename: str):
    title = title.strip()
    filename = filename.strip()
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response = stub.RequestToUpload(server_pb2.UploadToServerRequest(title=title, filename=filename))
        request_iterator = create_upload_iterator(filename)
        stub.UploadVideo(request_iterator)

    return response.ack
