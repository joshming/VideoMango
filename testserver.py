from pathlib import Path
import sqlite3

from serverpackage.videodatabase import VideoDatabase

import testingutils

table = "videos"
video_db = VideoDatabase("test")
location = "./videoDatabasetest.db"
columns = '(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, file TEXT, size INTEGER)'

def test_add_video_does_not_already_exist(filename: str, filenamebig: str):
    testingutils.clear_database(location, table)
    testingutils.createTable(location, table, columns)
    video_db.upload(filename, filenamebig, Path(filenamebig).stat().st_size)

    return len(video_db.get_all_videos()) == 1

def test_add_video_already_exists(filename: str, filenamebig: str):
    testingutils.clear_database(location, table)
    testingutils.createTable(location, table, columns)
    video_db.upload(filename, filenamebig, Path(filenamebig).stat().st_size)

    try:
        video_db.upload(filename, filenamebig, Path(filenamebig).stat().st_size)
    except (sqlite3.IntegrityError):
        return True

    return False

if __name__ == '__main__': 
    print(f"result test_add_video_does_not_already_exist: {test_add_video_does_not_already_exist("1MB", "1MB.mp4")}")
    print(f"result test_add_video_already_exists: {test_add_video_already_exists("1MB", "1MB.mp4")}")
