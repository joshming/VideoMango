import time
from concurrent import futures
from datetime import datetime

import google
import grpc

from comment import commentdatabase
from comment.Comment import Message
from proto import commentserver_pb2_grpc, commentserver_pb2


class CommentServerServicer(commentserver_pb2_grpc.CommentServerServicer):

    def __init__(self):
        commentdatabase.createTable()

    def send_message(self, request, context):
        video_id = request.video_id
        user = request.comment.user
        message = request.comment.message
        commentdatabase.add_message(video_id, Message(user, message, time.time_ns()))
        return google.protobuf.empty_pb2.Empty()

    def get_comments(self, request, context):
        video_id = request.video_id
        comments = commentdatabase.get_messages(video_id)
        if not comments:
            yield commentserver_pb2.CommentResponse(user="", message="", time="")
            return

        for comment in comments.messages:
            yield commentserver_pb2.CommentResponse(user=comment.user, message=comment.message, time=str(comment.time))


def serve(port: str) -> grpc.server:
    _server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    commentserver_pb2_grpc.add_CommentServerServicer_to_server(CommentServerServicer(), _server)
    _server.add_insecure_port(f'[::]:{port}')
    return _server


def main(port: str):
    _server = serve(port)
    _server.start()
    print(f"Starting Chat Server at {datetime.now()}")
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        _server.stop(0)