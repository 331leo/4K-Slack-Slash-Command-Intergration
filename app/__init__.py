from typing import Optional
from fastapi import FastAPI
from fastapi.param_functions import Depends
from dotenv import load_dotenv
load_dotenv()
import slack

app = FastAPI(
    title="C4K-Slack-Slash-Command-Intergration"
)
app.include_router(slack.router)

def gen_slack_message(text: str):
    return {"blocks":[{"type":"section","text":{"type":"mrkdwn","text":text}}]}

@app.get("/")
async def route_root():
    return {"message":"This is Slack Slash Command API for codefor.kr"}

@app.post("/createmail")
async def slash_createmail(slash: slack.SlashCommand = Depends()):
    print(slash)
    text = "hello world"
    return gen_slack_message(text)
