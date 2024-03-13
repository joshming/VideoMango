compile:
	python3.9 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./proto/server.proto ./proto/partyserver.proto;
