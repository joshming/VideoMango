import os
from typing import Dict, Any, List, Union

import google
import grpc

from clientpackage import cacheservice
from clientpackage.video import Video
from proto import server_pb2_grpc, server_pb2

VIDEO_EXTENSION = ".mp4"

cache_service = cacheservice.CacheService(60000)


def retrieve_all_movies() -> List[Dict[str, Any]]:
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response_iterator = stub.getAllVideos(google.protobuf.empty_pb2.Empty())
        videos = []
        for video in response_iterator:
            videos.append({"id": video.id, "title": video.title})
        return videos


def retrieve_movie_information(id_: int) -> Dict[str, Union[int, str]]:
    with grpc.insecure_channel('localhost:50051') as channel:
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
    print(start, end)
    totalChunks = cache_service.get_video(id_, start, end)
    if totalChunks:
        return totalChunks

    totalChunks = b''
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response_iterator = stub.StreamVideo(server_pb2.VideoRequest(videoId=id_))
        for response in response_iterator:
            totalChunks += response.chunk

    movie_info = retrieve_movie_information(id_)
    video = Video(id_, movie_info["title"], start, end, totalChunks[start:end + 1])
    cache_service.set_video(video)
    return video.get_bytes()