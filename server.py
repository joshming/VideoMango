import grpc

import server_pb2
import server_pb2_grpc
from videodatabase import VideoDatabase

CHUNK_SIZE = 1024 * 1024


class CdnServerServicer(server_pb2_grpc.CdnServerServicer):
    """
    The CDN server servicer that will handle file transfers to and from the client

    _videoDatabase: VideoDatabase
    """

    def __init__(self):
        self.videoDatabase = VideoDatabase()

    def StreamVideo(self, request, context):
        location = self.videoDatabase.fetch(request.videoId)
        with open(location, 'rb') as video:
            chunk = 1
            while chunk:
                chunk = video.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    return
                yield server_pb2.Chunk(chunk=chunk)

    def UploadVideo(self, request_iterator, context):
        # have to save it to the local storage
        pass