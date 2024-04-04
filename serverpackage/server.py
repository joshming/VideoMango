import signal
import sys
import threading
import time

from concurrent import futures
from datetime import datetime
from pathlib import Path
from typing import List

import google
import grpc
from grpc import server

from proto import server_pb2_grpc, server_pb2
from serverpackage.videodatabase import VideoDatabase

CHUNK_SIZE = 1024 * 1024
VIDEO_PATH = "./videos/"
VIDEO_EXTENSION = ".mp4"

OTHER_SERVER_PORTS = ["50051", "50052", "50053"]
REPLICATION_INTERVAL = 5


def get_titles(port: str) -> List[server_pb2.Title]:
    try:
        with grpc.insecure_channel('localhost:' + port) as channel:
            stub = server_pb2_grpc.CdnServerStub(channel)
            titles_iterator = stub.get_new_titles(google.protobuf.empty_pb2.Empty())
            if not titles_iterator:
                return []
            titles = [title for title in titles_iterator]
            return titles
    except grpc.RpcError:
        return []


class CdnServerServicer(server_pb2_grpc.CdnServerServicer):
    """
    The CDN server servicer that will handle file transfers to and from the client

    _videoDatabase: VideoDatabase
    """

    def __init__(self, port: str):
        self.different_ports = OTHER_SERVER_PORTS
        self.different_ports.remove(port)
        self.video_database = VideoDatabase(port)
        signal.signal(signal.SIGTERM, self.close_thread)
        self.replication_continue = True
        self.replication_thread = threading.Thread(target=self.replicate, daemon=True)
        self.replication_thread.start()

    def close_thread(self):
        self.replication_continue = False

    def getAllVideos(self, request, context):
        result = self.video_database.get_all_videos()
        for row in result:
            yield server_pb2.VideoInfo(id=row[0], title=row[1])

    def getVideoInformation(self, request, context):
        result = self.video_database.get_video_information(request.videoId)
        if not result:
            return server_pb2.VideoInfo(id=-1, title="", size=-1)
        return server_pb2.VideoInfo(id=result[0], title=result[1], size=result[2])

    def StreamVideo(self, request, context):
        video = self.video_database.fetch(request.videoId)
        location = VIDEO_PATH + video[1] + VIDEO_EXTENSION
        with open(location, 'rb') as file:
            while True:
                chunk = file.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    return
                yield server_pb2.Chunk(chunk=chunk)

    def RequestToUpload(self, request, context):
        title = request.title
        filename = request.filename
        size = Path(filename + VIDEO_EXTENSION).stat().st_size
        if self.video_database.checkTitle(title):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return server_pb2.UploadResponse(ack="ERROR")

        self.video_database.upload(title, filename, size)
        return server_pb2.UploadResponse(ack="OK")

    def UploadVideo(self, request_iterator, context):
        # have to save it to the local storage
        file = self.video_database.get_most_recent_file()
        self._save(request_iterator, file + VIDEO_EXTENSION)
        return server_pb2.UploadResponse(ack="OK")

    def _save(self, chunks, filename):
        with open(VIDEO_PATH + filename, 'wb') as f:
            for chunk in chunks:
                f.write(chunk.chunk)
        print(f"uploaded {filename}")

    def get_video(self, request, context):
        title = request.title
        video = self.video_database.fetch_by_title(title)
        location = VIDEO_PATH + video[0] + VIDEO_EXTENSION
        print("sending video with location " + location)
        with open(location, 'rb') as file:
            while True:
                chunk = file.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    return
                yield server_pb2.Chunk(chunk=chunk)

    def get_new_titles(self, request, context):
        videos = self.video_database.get_recently_added()
        for title, size in videos:
            yield server_pb2.Title(title=title, size=size)

    def retrieve_video(self, port: str, title: str, size: int) -> None:
        if self.video_database.checkTitle(title):
            return
        self.video_database.upload(title, title, size)
        print("retrieving the video " + title)
        with grpc.insecure_channel('localhost:' + port) as channel:
            stub = server_pb2_grpc.CdnServerStub(channel)
            video_chunks = stub.get_video(server_pb2.Title(title=title))
            self._save(video_chunks, title + VIDEO_EXTENSION)

    def replicate(self) -> None:
        try:
            while self.replication_continue:
                print("replicating...")
                for port in self.different_ports:
                    titles = get_titles(port)
                    for video in titles:
                        title = video.title
                        size = video.size
                        self.retrieve_video(port, title, size)
                time.sleep(REPLICATION_INTERVAL)
        except KeyboardInterrupt:
            return


def serve(port: str) -> server:
    _server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_CdnServerServicer_to_server(CdnServerServicer(port), _server)
    _server.add_insecure_port(f'[::]:{port}')
    return _server


def main(port: str):
    print(f"Starting CDN at {datetime.now()}")
    _server = serve(port)
    _server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        _server.stop(0)
