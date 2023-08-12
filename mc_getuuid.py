#!/usr/bin/env python3
import requests
import uuid
import json

def getuuid(username):
    BASE_URL = "https://api.mojang.com/users/profiles/minecraft/"
    FINAL_URL = BASE_URL + str(username)
    req = requests.get(FINAL_URL)
    obj = req.json()
    # Deal with errors
    if int(req.status_code) != 200:
        return False
    uid = obj['id']
    # Format UUID
    formatted_uid = str(uuid.UUID(uid))
    return formatted_uid