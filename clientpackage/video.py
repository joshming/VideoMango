import datetime
import time

NANOSECOND_CONVERSION = 1000000


class Video:
    """
    Represents a video

    _id: int = video id
    _title: str = video title
    _start: int = bytes start from total size of video
    _end: int = bytes end from total size of video
    _bytes: byte
    _ttl: a time to live for the bytes, equal to 60 seconds in the future
    """

    def __init__(self, id_: int, title: str, start: int, end: int, bytes_: bytes):
        self._id = id_
        self._title = title
        self._start = start
        self._end = end
        self._bytes = bytes_
        self._ttl = time.time_ns() // NANOSECOND_CONVERSION + 60000

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_bytes(self):
        return self._bytes

    def get_ttl(self):
        return self._ttl