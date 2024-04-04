import grpc

from comment.Comment import Comment, Message
from proto import commentserver_pb2_grpc, commentserver_pb2

CHAT_PORT = "50070"

def send_message(video_id: int, user: str, message: str):
    # to make this infinite, maybe the channel cannot be closed,
    with grpc.insecure_channel('localhost:' + CHAT_PORT) as channel:
        stub = commentserver_pb2_grpc.CommentServerStub(channel)
        stub.send_message(
            commentserver_pb2.SendComment(video_id=video_id, comment=commentserver_pb2.Comment(user=user, message=message)))


def get_messages(video_id: int) -> Comment:
    with grpc.insecure_channel('localhost:' + CHAT_PORT) as channel:
        stub = commentserver_pb2_grpc.CommentServerStub(channel)
        users = set()
        comments = Comment([], [], video_id)
        comments_iterator = stub.get_comments(commentserver_pb2.Video(video_id=video_id))
        for comment in comments_iterator:
            if comment.user == "":
                return comments
            message = Message(comment.user, comment.message, int(comment.time))
            if comment.user not in users:
                users.add(comment.user)
                comments.users.append(comment.user)
            comments.messages.append(message)

        return comments
