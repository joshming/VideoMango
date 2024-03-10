import gzip
from typing import Dict, Any

import google
import grpc

from clientpackage.fileutils.fileutils import compress, decompress
from proto import server_pb2_grpc, server_pb2

CHUNK_SIZE = 1024 * 1024


def create_upload_iterator(filename: str):
    with open("./videos/" + filename + ".gz", 'rb') as compressed_file:
        while True:
            chunk = compressed_file.read(CHUNK_SIZE)
            if len(chunk) == 0:
                return
            yield server_pb2.UploadRequest(chunk=server_pb2.Chunk(chunk=chunk))


def upload(title: str, filename: str) -> bool:
    title = title.strip()
    filename = filename.strip()
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response = stub.RequestToUpload(server_pb2.UploadToServerRequest(title=title, filename=filename))

        compress(filename)
        request_iterator = create_upload_iterator(filename)
        stub.UploadVideo(request_iterator)
    return response.ack


def get_all_video_information():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response_iterator = stub.getAllVideos(google.protobuf.empty_pb2.Empty())
        print(response_iterator)
        videos = []
        for video in response_iterator:
            videos.append({video.id: video.title})
        return videos


def get_movie_information_by_id(id: int) -> Dict[str, Any]:
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response = stub.getVideoInformation(server_pb2.VideoRequest(videoId=id))
        return {"id": response.id, "title": response.title}


def retrieve_video(title: str):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response_iterator = stub.StreamVideo(server_pb2.VideoRequest(title=title))
        pass
