import asyncio
import aiohttp
import json
import os

MAIL_ADMIN_BASE_URL = "https://" + os.environ.get("mail_server_domain") + "/admin"

class AdminClient:
    def __init__(self):
        self.users_cache = list()
        pass

    async def get_all_users(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                MAIL_ADMIN_BASE_URL + "/mail/users",
                auth=aiohttp.BasicAuth(os.environ.get("mail_admin_api_id"),os.environ.get("mail_admin_api_password")),
                params={"format":"json"}
            ) as resp:
                assert resp.status == 200, "get_all_users, Response Code is not 200. Current Response code is {}".format(resp.status)
                data = await resp.json()
                users = list()
                for domain in data:
                    for user in domain.get("users", None):
                        if user.get("status",None) == "active": users.append(user.get("email"))
                self.users_cache = users
                return users
