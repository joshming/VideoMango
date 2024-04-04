import random

import google
import grpc

from typing import Dict, Any, List, Union

from clientpackage import cacheservice
from clientpackage.video import Video
from proto import server_pb2_grpc, server_pb2, authentication_pb2_grpc, authentication_pb2

SERVER_PORTS = ('50051', '50052', '50053')
AUTHENTICATION_PORT = '50060'
cache_service = cacheservice.CacheService(60000)

CHUNK_SIZE = 1024 * 1024
VIDEO_EXTENSION = ".mp4"


def choose_cdn_server_port() -> str:
    for port in SERVER_PORTS:
        try:
            print(f"trying {port}")
            channel = grpc.insecure_channel(f'localhost:{port}')
            stub = server_pb2_grpc.CdnServerStub(channel)
            stub.getVideoInformation(server_pb2.VideoRequest(videoId=1))
            print("connection secured")
            return port
        except:
            pass
    exit(1)


def retrieve_all_movies() -> List[Dict[str, Any]]:
    with grpc.insecure_channel('localhost:' + choose_cdn_server_port()) as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response_iterator = stub.getAllVideos(google.protobuf.empty_pb2.Empty())
        videos = []
        for video in response_iterator:
            videos.append({"id": video.id, "title": video.title})
        return videos


def retrieve_movie_information(id_: int) -> Dict[str, Union[int, str]]:
    with grpc.insecure_channel('localhost:' + choose_cdn_server_port()) as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response = stub.getVideoInformation(server_pb2.VideoRequest(videoId=id_))
        return {"id": response.id, "title": response.title, "size": response.size}


def get_video_bytes_for_stream(id_: int, start: int, end: int) -> bytes:
    """
    Streams the requested movie using the <id> that has been passed in
    each set of bytes returned are considered partial content as the entire video is not sent back to the client,
    only the amount specified in the range.

    range is part of the header that is automatically sent from the frontend

    :param id_: the id of the video
    :param start: start of the byte sequence
    :param end: end of the byte sequence
    :return: a video bytes
    """
    totalChunks = cache_service.get_video(id_, start, end)
    if totalChunks:
        return totalChunks

    totalChunks = b''
    with grpc.insecure_channel('localhost:' + choose_cdn_server_port()) as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response_iterator = stub.StreamVideo(server_pb2.VideoRequest(videoId=id_))
        for response in response_iterator:
            totalChunks += response.chunk

    movie_info = retrieve_movie_information(id_)
    video = Video(id_, movie_info["title"], start, end, totalChunks[start:end + 1])
    cache_service.set_video(video)
    return video.get_bytes()


def create_upload_iterator(filename: str):
    filename = filename + VIDEO_EXTENSION
    with open(filename, 'rb') as compressed_file:
        while True:
            chunk = compressed_file.read(CHUNK_SIZE)
            if len(chunk) == 0:
                return
            yield server_pb2.Chunk(chunk=chunk)


def upload(title: str, filename: str):
    title = title.strip()
    filename = filename.strip()
    with grpc.insecure_channel('localhost:' + choose_cdn_server_port()) as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response = stub.RequestToUpload(server_pb2.UploadToServerRequest(title=title, filename=filename))
        request_iterator = create_upload_iterator(filename)
        stub.UploadVideo(request_iterator)
        return response


def create_user(username: str, password: str):
    with grpc.insecure_channel('localhost:' + AUTHENTICATION_PORT) as channel:
        stub = authentication_pb2_grpc.AuthenticationStub(channel)
        return stub.create_account(authentication_pb2.AccountRequest(username=username, password=password))


def login(username: str, password: str):
    with grpc.insecure_channel('localhost:' + AUTHENTICATION_PORT) as channel:
        stub = authentication_pb2_grpc.AuthenticationStub(channel)
        return stub.login(authentication_pb2.AccountRequest(username=username, password=password))


def is_authenticated(token: int, username: str) -> bool:
    with grpc.insecure_channel('localhost:' + AUTHENTICATION_PORT) as channel:
        stub = authentication_pb2_grpc.AuthenticationStub(channel)
        return stub.is_authenticated(
            authentication_pb2.AuthenticationRequest(token=token, username=username)).can_log_in
