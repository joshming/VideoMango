import gzip

import grpc

from clientpackage.fileutils.fileutils import compress, decompress
from proto import server_pb2_grpc, server_pb2

CHUNK_SIZE = 1024 * 1024


def create_upload_iterator(filename: str):
    with open("./videos/" + filename + ".gz", 'rb') as compressed_file:
        while True:
            chunk = compressed_file.read(CHUNK_SIZE)
            if len(chunk) == 0:
                return
            yield server_pb2.UploadRequest(chunk=server_pb2.Chunk(chunk=chunk))


def upload(title: str, filename: str) -> bool:
    title = title.strip()
    filename = filename.strip()
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.CdnServerStub(channel)
        response = stub.RequestToUpload(server_pb2.UploadToServerRequest(title=title, filename=filename))

        compress(filename)
        request_iterator = create_upload_iterator(filename)
        stub.UploadVideo(request_iterator)
    return response.ack


def main():
    try:
        while True:
            title = input("What is the title of the movie: ")
            filename = input("filename: ")
            print(upload(title, filename))
            decompress(filename)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
