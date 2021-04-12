from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

import slack
from .commands import router as commands_router


app = FastAPI(
    title="C4K-Slack-Slash-Command-Integration"
)

app.include_router(slack.router)
app.include_router(commands_router)


@app.get("/")
async def route_root():
    return {"message":"This is Slack Slash Command API for codefor.kr"}