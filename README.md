# Video Mango 

A video streaming platform to allow you and your friends watch movies together 

## Tech
- Python 3.9+
- gRPC
- fastAPI

## Run instructions
To start the backend server
```{shell}
python startserver.py
```

to start the REST API
```{shell}
uvicorn clientpackage.clientapi:app --reload
```