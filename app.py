from typing import Optional
from fastapi import FastAPI
from fastapi.param_functions import Depends
from dotenv import load_dotenv
load_dotenv()
import slack_util

app = FastAPI()
app.include_router(slack_util.router)

def gen_slack_message(text: str):
    return {"blocks":[{"type":"section","text":{"type":"mrkdwn","text":text}}]}

@app.get("/")
def route_root():
    return {"message":"This is Slack Slash Command API for codefor.kr"}

@app.post("/createmail")
def slash_createmail(slash: slack_util.SlashCommand = Depends()):
    print(slash)
    text = "hello world"
    return gen_slack_message(text)
