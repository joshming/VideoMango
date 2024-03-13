import time
from concurrent import futures
from datetime import datetime

import grpc
from grpc import server

from proto import partyserver_pb2, partyserver_pb2_grpc

class PartyServerServicer(partyserver_pb2_grpc.PartyServerServicer()):
    pass

def serve() -> server:
    _server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    partyserver_pb2_grpc.add_PartyServerServicer_to_server(PartyServerServicer(), _server)
    _server.add_insecure_port('[::]:50052')
    return _server


def main():
    print(f"Starting Party Server at {datetime.now()}")
    _server = serve()
    _server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        _server.stop(0)


if __name__ == '__main__':
    main()