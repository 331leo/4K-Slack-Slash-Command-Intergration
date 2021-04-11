from dotenv import load_dotenv
load_dotenv()

from typing import Optional
from fastapi import FastAPI
from fastapi.param_functions import Depends

import slack
from mail import AdminClient

app = FastAPI(
    title="C4K-Slack-Slash-Command-Intergration"
)
app.include_router(slack.router)

MailApi = AdminClient()

def gen_slack_message(text: str):
    return {"blocks":[{"type":"section","text":{"type":"mrkdwn","text":text}}]}

@app.on_event("startup")
async def on_startup():
    await MailApi.get_all_users()

@app.get("/")
async def route_root():
    return {
            "message":"This is Slack Slash Command API for codefor.kr"}

@app.post("/createmail")
async def slash_createmail(slash: slack.SlashCommand = Depends()):
    print(slash)
    text = "hello world"
    return gen_slack_message(text)
