import time

from concurrent import futures
from datetime import datetime

import grpc
from grpc import server

from proto import server_pb2_grpc, server_pb2
from serverpackage.videodatabase import VideoDatabase

CHUNK_SIZE = 1024 * 1024


class CdnServerServicer(server_pb2_grpc.CdnServerServicer):
    """
    The CDN server servicer that will handle file transfers to and from the client

    _videoDatabase: VideoDatabase
    """

    def __init__(self):
        self.video_database = VideoDatabase()

    def StreamVideo(self, request, context):
        location = self.video_database.fetch(request.videoId)
        with open(location, 'rb') as video:
            chunk = 1
            while chunk:
                chunk = video.read(CHUNK_SIZE)
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
        self._save(request_iterator, file + ".gz")
        return server_pb2.UploadResponse(ack="OK")

    def _save(self, chunks, filename):
        with open(filename, 'wb') as f:
            for chunk in chunks:
                f.write(chunk.chunk.chunk)


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
