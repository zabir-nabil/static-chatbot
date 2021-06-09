from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

import uvicorn
import json

app = FastAPI()
app.user_msgs = json.load(open("user_msgs.json"))
app.bot_responses = json.load(open("bot_responses.json"))
app.chat_schema = json.load(open("chat.json"))
app.start_chat = "start"


class Chat(BaseModel):
    id_: str # conv id
    msg: str


@app.get("/")
def read_root():
    return {"msg": "The chat server is live!", "success": 1}


@app.post("/chat/bot")
def bot_response(chat: Chat):
    # start message with "start"
    try:
        if chat.msg == app.start_chat:
            return app.bot_responses["b_hi"]
        else:
            # find the key for the text
            # searching is inefficient
            for k, v in app.user_msgs.items():
                for i, b in enumerate(v["buttons"]):
                    if chat.msg == b:
                        # now I know, both key and index
                        br_key = app.chat_schema[k][i]
                        return app.bot_responses[br_key]
            
            return {"text": "We could not process your query. It will be sent to the system as an error."}
    except Exception as e:
        print(e)
        return {"text": "We could not process your query. It will be sent to the system as an error."}


@app.post("/chat/user")
def user_buttons(chat: Chat):
    try:
        # find the key for the text
        # searching is inefficient
        for k, v in app.bot_responses.items():
            if chat.msg == v["text"]:
                # now I know, key
                um_key = app.chat_schema[k][0]
                return app.user_msgs[um_key]
            
        return {"text": "We could not process your query. It will be sent to the system as an error."}
    except Exception as e:
        print(e)
        return {"text": "We could not process your query. It will be sent to the system as an error."}


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')