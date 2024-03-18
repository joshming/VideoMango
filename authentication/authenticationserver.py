import time
from concurrent import futures
from datetime import datetime

import grpc
from grpc import server

from authentication import userdatabase
from proto import authentication_pb2_grpc, authentication_pb2


AUTHENTICATED_USER_CACHE = {}


class AuthenticationServerServicer(authentication_pb2_grpc.AuthenticationServicer):

    def __init__(self):
        userdatabase.createTable()

    def create_account(self, request, context):
        username = request.username
        password = request.password
        if not userdatabase.create_user(username, password):
            return authentication_pb2.AccountResponse(can_log_in=False, userId=-1, message="User already exists")
        user_information = userdatabase.get_user_information(username)
        AUTHENTICATED_USER_CACHE[user_information[0]] = username
        return authentication_pb2.AccountResponse(can_log_in=True, userId=user_information[0], message="OK")

    def login(self, request, context):
        username = request.username
        password = request.password
        if not userdatabase.verify_user(username, password):
            return authentication_pb2.AccountResponse(can_log_in=False, userId=-1, message="Incorrect username or password")
        user_information = userdatabase.get_user_information(username)
        AUTHENTICATED_USER_CACHE[user_information[0]] = username
        return authentication_pb2.AccountResponse(can_log_in=True, userId=user_information[0], message="OK")

    def is_authenticated(self, request, context):
        token = request.token
        username = request.username

        if token in AUTHENTICATED_USER_CACHE and AUTHENTICATED_USER_CACHE[token] == username:
            return authentication_pb2.AuthenticationResponse(can_log_in=True)
        return authentication_pb2.AuthenticationResponse(can_log_in=False)


def serve(port: str) -> server:
    _server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    authentication_pb2_grpc.add_AuthenticationServicer_to_server(AuthenticationServerServicer(), _server)
    _server.add_insecure_port(f'[::]:{port}')
    return _server


def main(port: str):
    print(f"Starting Authentication Server at {datetime.now()}")
    _server = serve(port)
    _server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        _server.stop(0)
