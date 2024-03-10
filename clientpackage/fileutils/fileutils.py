import gzip
import shutil

VIDEOS_PATH = "./videos/"
CLIENT_PATH = "./clientvideos/"
CURRENT_EXTENSION = ".mp4"

CHUNK_SIZE = 1024 * 1024


def compress(filename: str) -> None:
    """
    Compresses file to a gzip file
    :param filename: the name of the file
    :return:
    """
    with open(filename + CURRENT_EXTENSION, 'rb') as file:
        with gzip.open("./videos/" + filename + ".gz", "wb") as compressed:
            compressed.writelines(file)


def decompress(filename: str) -> None:
    with gzip.open(filename + ".gz", 'rb') as compressed:
        with open(CLIENT_PATH + filename + CURRENT_EXTENSION, 'wb') as decompressed:
            shutil.copyfileobj(compressed, decompressed)
    print("done")
