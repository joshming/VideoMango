import threading
import time
from typing import Any, Optional, Dict

from clientpackage.video import Video

condition = threading.Event()


class CacheService:
    """
    Creates a caching service that is responsible for caching an object

    _cache is the actual cache
    _ttl is the configured time to live of that object in milliseconds
    """
    _cache: Dict[int, Dict[str, Video]]
    _ttl: int

    def __init__(self, ttl: int):
        self._cache = {}
        self._ttl = ttl

    def get_video(self, id_: int, start: int, end: int) -> Optional[bytes]:
        if id_ in self._cache and f"{start},{end}" in self._cache[id_]:
            video = self._cache[id_][f"{start},{end}"]
            if (time.time_ns() // 1000000) >= video.get_ttl():
                self._cache[id_].pop(f"{start},{end}")
                return None
            return self._cache[id_][f"{start},{end}"].get_bytes()

        return None

    def set_video(self, video: Video) -> None:
        self._cache[video.get_id()] = {f"{video.get_start()},{video.get_end()}": video}
