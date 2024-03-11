import time

from concurrent import futures
from datetime import datetime

import grpc
from grpc import server

from proto import server_pb2_grpc, server_pb2
from serverpackage.videodatabase import VideoDatabase

CHUNK_SIZE = 1024 * 1024
VIDEO_PATH = "./videos/"


class CdnServerServicer(server_pb2_grpc.CdnServerServicer):
    """
    The CDN server servicer that will handle file transfers to and from the client

    _videoDatabase: VideoDatabase
    """

    def __init__(self):
        self.video_database = VideoDatabase()

    def getAllVideos(self, request, context):
        result = self.video_database.get_all_videos()
        for row in result:
            yield server_pb2.VideoInfo(id=row[0], title=row[1])

    def getVideoInformation(self, request, context):
        result = self.video_database.get_video_information(request.videoId)
        return server_pb2.VideoInfo(id=result[0], title=result[1])

    def StreamVideo(self, request, context):
        video = self.video_database.fetch(request.videoId)
        location = VIDEO_PATH + video[1] + ".mp4"
        title = video[0]
        with open(location, 'rb') as file:
            while True:
                chunk = file.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    return
                yield server_pb2.Chunk(chunk=chunk)

    def RequestToUpload(self, request, context):
        title = request.title
        filename = request.filename
        if self.video_database.checkTitle(title):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return server_pb2.UploadResponse(ack="ERROR")

        self.video_database.upload(title, filename)
        return server_pb2.UploadResponse(ack="OK")

    def UploadVideo(self, request_iterator, context):
        # have to save it to the local storage
        file = self.video_database.get_most_recent_file()
        self._save(request_iterator, file + ".mp4")
        return server_pb2.UploadResponse(ack="OK")

    def _save(self, chunks, filename):
        with open(VIDEO_PATH + filename, 'wb') as f:
            for chunk in chunks:
                f.write(chunk.chunk)


def serve() -> server:
    _server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_CdnServerServicer_to_server(CdnServerServicer(), _server)
    _server.add_insecure_port('[::]:50051')
    return _server


def main():
    print(f"Starting CDN at {datetime.now()}")
    _server = serve()
    _server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        _server.stop(0)


if __name__ == '__main__':
    main()
