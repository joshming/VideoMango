# MeerkatVideo

A video streaming platform to allow you and your friends watch movies together 

## Tech
- Python 3.9+
- gRPC
- fastAPI
- SQLite3
- NextJS

## Run instructions
To start the backend server
```{shell}
python startserver.py
```

To start the frontend, assuming in root directory `VideoMango`
```{shell}
cd ./frontend/meerkat-video; npm run dev
```

to start the REST API
```{shell}
uvicorn clientpackage.clientapi:app --reload
```