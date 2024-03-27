from datetime import datetime
from typing import List


class Message:
    user: str
    message: str
    time: int

    def __init__(self, user: str, message: str, time: int):
        self.user = user
        self.message = message
        self.time = time

    def to_dictionary(self):
        return {"user": self.user, "message": self.message, "time": self.time}

    def to_response_dictionary(self):
        return {"user": self.user, "message": self.message, "time": datetime.fromtimestamp(self.time // 1000000000)}


class Comment:
    users: List[str]
    messages: List[Message]
    video_id: int

    def __init__(self, users: List[str], messages: List[Message], video_id: int):
        self.users = users
        self.messages = messages
        self.video_id = video_id

    def to_dictionary(self):
        return {"users": self.users, "messages": [message.to_dictionary() for message in self.messages]}

    def to_response_dictionary(self):
        return {"users": self.users, "messages": [message.to_response_dictionary() for message in self.messages]}
