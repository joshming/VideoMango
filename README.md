# MeerkatVideo

A video streaming platform to allow you and your friends watch movies together

## Tech
- Python 3.9+
- gRPC
- fastAPI
- SQLite3
- NextJS

## Run instructions

To upload a video, have the video in the root directory then run the curl (replacing the information)
```{shell}
curl --location --request POST 'http://127.0.0.1:8000/upload?title=Meerkat%20Facts&filename=meerkat-facts'
```

To start the backend server, select some port in `{ 50051, 50052, 50053 }` and include it in the below script
```{shell}
python startserver.py <port>
```

To Start the authentication server, 
```{shell}
python startserver.py 50060
```

To start the frontend, assuming in root directory `VideoMango`
```{shell}
cd ./frontend/meerkat-video; npm run dev
```

to start the REST API
```{shell}
uvicorn clientpackage.clientapi:app --reload
```