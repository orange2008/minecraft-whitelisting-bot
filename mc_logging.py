#!/usr/bin/env python3
import datetime
from mc_database import timestamp

def log_info(log_content):
    TO_BE_WRITTEN = timestamp() + ", info, " + str(log_content)
    print(TO_BE_WRITTEN)
    with open("system.log", 'a') as log:
        log.write(TO_BE_WRITTEN + "\n")
    return True

def log_warning(log_content):
    TO_BE_WRITTEN = timestamp() + ", warning, " + str(log_content)
    print(TO_BE_WRITTEN)
    with open("system.log", 'a') as log:
        log.write(TO_BE_WRITTEN + "\n")
    return True

def log_botstart():
    log_content = "Bot started."
    log_info(log_content)
    return True

def log_start(telegram_id):
    log_content = "User " + str(telegram_id) + " started the bot."
    log_info(log_content)
    return True

def log_add_to_whitelist(telegram_id, minecraft_id):
    log_content = "User " + str(telegram_id) + " added " + str(minecraft_id) + " to the whitelist."
    log_info(log_content)
    return True

def log_delete_from_whitelist(telegram_id, minecraft_id):
    log_content = "User " + str(telegram_id) + " deleted " + str(minecraft_id) + " from the whitelist."
    log_info(log_content)
    return True

def log_show_themselves(telegram_id, minecraft_id):
    log_content = "User " + str(telegram_id) + " requested their Minecraft ID, which is " + str(minecraft_id)
    log_info(log_content)
    return True

def log_show_themselves_but_not_exist(telegram_id):
    log_content = "User " + str(telegram_id) + " requested their Minecraft ID, but they never registered it."
    log_warning(log_content)
    return True

def log_invalid_user(telegram_id, minecraft_id):
    log_content = "User " + str(telegram_id) + " tried to add " + str(minecraft_id) + " to the whitelist, but the user was never existed."
    log_warning(log_content)
    return True

def log_add_to_whitelist_but_exist(telegram_id, minecraft_id):
    log_content = "User " + str(telegram_id) + " tried to add " + str(minecraft_id) + " to the whitelist, but it already have an account registered."
    log_warning(log_content)
    return True

def log_delete_from_whitelist_but_not_exist(telegram_id, minecraft_id):
    log_content = "User " + str(telegram_id) + " tried to delete " + str(minecraft_id) + " from the whitelist, but the user was never in the whitelist."
    log_warning(log_content)
    return True