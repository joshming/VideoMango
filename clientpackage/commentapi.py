from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from clientpackage import commentservice

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    user: str
    message: str


@app.post("/comment/{id_}")
async def send_message(id_: int, message: MessageRequest):
    commentservice.send_message(id_, message.user, message.message)
    return Response(status_code=201)


@app.get("/comment/{id_}")
async def get_chat(id_: int):
    results = commentservice.get_messages(id_)
    return results.to_response_dictionary()
