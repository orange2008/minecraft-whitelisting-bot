#!/usr/bin/env python3
from mcrcon import MCRcon
import json
import requests

import mc_getuuid


def readconfig():
    with open("./config.json") as f:
        conf = json.load(f)
    # Construct list
    rconconf = [conf['rcon_host'], conf['rcon_port'], conf['rcon_password']]
    return rconconf

def add_to_whitelist(username):
    # Read configuration
    rconconf = readconfig()
    RCON_HOSTNAME = str(rconconf[0])
    RCON_PORT = int(rconconf[1])
    RCON_PASSWORD = str(rconconf[2])
    TO_BE_ADDED = str(username)
    # Get UUID
    uid = mc_getuuid.getuuid(str(username))
    if uid == None:
        # The user doesn't exist
        return False
    # Open RCON session
    with MCRcon(RCON_HOSTNAME, RCON_PASSWORD, port=RCON_PORT) as mcr:
        resp = mcr.command("/whitelist add " + str(TO_BE_ADDED))
    if "from the whitelist" in resp:
        # Everything's good.
        return True

def remove_from_whitelist(username):
    # Read configuration
    rconconf = readconfig()
    RCON_HOSTNAME = str(rconconf[0])
    RCON_PORT = int(rconconf[1])
    RCON_PASSWORD = str(rconconf[2])
    TO_BE_REMOVED = str(username)
    # Get UUID
    uid = mc_getuuid(str(username))
    if uid == None:
        # The user doesn't exist
        return False
    # Open RCON session
    with MCRcon(RCON_HOSTNAME, RCON_PASSWORD, port=RCON_PORT) as mcr:
        resp = mcr.command("/whitelist remove " + str(TO_BE_REMOVED))
    if "from the whitelist" in resp:
        # Everything's good.
        return True
