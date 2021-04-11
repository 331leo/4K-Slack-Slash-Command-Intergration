import asyncio
import aiohttp
import json
import os
import random
from exceptions import *

MAIL_ADMIN_BASE_URL = "https://" + os.environ.get("mail_server_domain") + "/admin"

class AdminClient:
    def __init__(self):
        self.users_cache = list()
        self.domain_cache = list()
        self.auth=aiohttp.BasicAuth(os.environ.get("mail_admin_api_id"),os.environ.get("mail_admin_api_password"))
        pass

    async def get_all_users(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                MAIL_ADMIN_BASE_URL + "/mail/users",
                auth=self.auth,
                params={"format":"json"}
            ) as resp:
                assert resp.status == 200, "get_all_users, Response Code is not 200. Current Response code is {}".format(resp.status)
                data = await resp.json()
                users = list()
                domains = list()
                for domain in data:
                    domains.append(domain.get("domain"))
                    for user in domain.get("users", None):
                        if user.get("status",None) == "active": users.append(user.get("email"))
                self.users_cache = users
                self.domain_cache = domains
                return users
    
    async def post_new_user(self, email):
        if email in self.users_cache:
            raise AlreadyExsistingEmail(email)

        if len(email.split("@")) != 2:
            raise InvaildInput(email)
        
        id = email.split("@")[0]
        domain = email.split("@")[1]
        
        if domain not in self.domain_cache:
            raise InvaildDomain(domain)
        

        generated_password = ""
        for _ in range(9):
            generated_password += random.choice(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))

        
        payload = {"email":email, "password":generated_password}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                MAIL_ADMIN_BASE_URL + "/mail/users/add",
                data=payload,
                auth=self.auth
            ) as resp:
                if await resp.text() == "Invalid email address.":
                        raise InvaildInput(email)
                assert resp.status == 200, "post_new_user, Response Code is not 200. Current Response code is {}".format(resp.status)
                self.users_cache.append(email)
                return payload
