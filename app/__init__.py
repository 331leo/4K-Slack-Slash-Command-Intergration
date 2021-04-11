from dotenv import load_dotenv
load_dotenv()

from typing import Optional
from fastapi import FastAPI
from fastapi.param_functions import Depends
from redis import Redis
import os

import slack
from mail import AdminClient
from exceptions import *
app = FastAPI(
    title="C4K-Slack-Slash-Command-Intergration"
)
app.include_router(slack.router)

MailApi = AdminClient()

db = Redis(host="localhost", port=6379, db=0)

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
    try:
        if db.get(slash.user_id):
            raise AlreadyExsistingUser(slash.user_id, db.get(slash.user_id).decode())
        data = await MailApi.post_new_user(slash.text)
        if data:
            text = f"""
성공적으로 이메일 발급에 성공하였습니다!
아래 인증정보를 통해 웹 메일에 로그인 하실 수 있습니다.
로그인 후, `설정->암호` 에서 비밀번호를 꼭 변경 후 사용하시기 바랍니다.

https://{os.environ.get("mail_server_domain")}
```
ID: {data.get("email")}
PW: {data.get("password")}
```

다른 메일 클라이언트를 사용하시려면 아래 설정을 입력하세요.
```
받는 메일 서버(IMAP): {os.environ.get("mail_server_domain")} (기본포트 993)
보내는 메일 서버(SMTP): {os.environ.get("mail_server_domain")} (기본포트 587)
Username: 이메일 주소 전체
Password: 비밀번호
```
            """
            db.set(slash.user_id,data.get("email"))
            return gen_slack_message(text)
    except AlreadyExsistingUser as e:
        print(e.text)
        return gen_slack_message(e.text)
    except AlreadyExsistingEmail as e:
        print(e.text)
        return gen_slack_message(e.text)
    except InvaildInput as e:
        print(e.text)
        return gen_slack_message(e.text)
    except InvaildDomain as e:
        print(e.text)
        return gen_slack_message(e.text)
    except Exception as e:
        raise e