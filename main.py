#!/usr/bin/env python3
# Author: Frank Ruan
# Licensed under MIT

import json
import asyncio
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import mc_whitelist
import mc_database
import mc_getuuid
import mc_logging

# Read bot token
with open("config.json") as f:
    conf = json.load(f)
TOKEN = conf['bot_token']

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Welcome to Prism's Minecraft Server. \nThe Server has whitelist turned on, so you will need to register your Minecraft account using this bot.\nNote that the Telegram account will be tied to your Minecraft account.\nYou are responsible for everything you are going to do in the server and we reserve the right to bring proceedings in the courts of the Hong Kong Special Administrative Region.")
    mc_logging.log_start(str(update.message.from_user.id))

def register(update: Update, context: CallbackContext) -> None:
    telegram_id = update.message.from_user.id
    telegram_id = str(telegram_id)
    minecraft_id = ' '.join(context.args)
    minecraft_id = str(minecraft_id)
    if mc_database.check_not_exist_by_telegram_id(telegram_id):
        pass
    else:
        # User already exists.
        update.message.reply_text("You already have an account registered.\nUnable to register.")
        mc_logging.log_add_to_whitelist_but_exist(telegram_id)
        return False
    update.message.reply_text("You are about to register your Minecraft account with playerID " + minecraft_id + " on our server.")
    # Deprecated, because something weird could happen.
    # loops = asyncio.get_event_loop()
    try:
        loops = asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            loops = asyncio.new_event_loop()
            asyncio.set_event_loop(loops)
    status = loops.run_until_complete(mc_whitelist.add_to_whitelist(minecraft_id))
    if status == True:
        # Completed, now add to database.
        minecraft_uuid = mc_getuuid.getuuid(minecraft_id)
        mc_database.insert(telegram_id, minecraft_id, minecraft_uuid)
        update.message.reply_text("Completed! We have just added your account to the whitelist. Launch your game and enjoy!")
        mc_logging.log_add_to_whitelist(telegram_id, minecraft_id)
        return True
    elif status == False:
        # User doesn't exist
        update.message.reply_text("We cannot verify the existence of your account.\nPlease check the username you have submitted.")
        mc_logging.log_invalid_user(telegram_id, minecraft_id)
        return False
    
def remove(update: Update, context: CallbackContext) -> None:
    telegram_id = update.message.from_user.id
    telegram_id = str(telegram_id)
    if mc_database.check_not_exist_by_telegram_id(telegram_id):
        update.message.reply_text("You never registered an account, thus you don't need to delete it.")
        mc_logging.log_delete_from_whitelist_but_not_exist(telegram_id, minecraft_id)
        return False
    # Fetch the player ID with Telegram ID
    # The value should be a tuple
    minecraft_id = mc_database.fetch_minecraft_id_by_telegram_id(telegram_id)
    update.message.reply_text("You are about to delete your Minecraft account with playerID " + minecraft_id + " on our server.")
    # Deprecated, because something weird could happen.
    # loops = asyncio.get_event_loop()
    try:
        loops = asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            loops = asyncio.new_event_loop()
            asyncio.set_event_loop(loops)
    status = loops.run_until_complete(mc_whitelist.remove_from_whitelist(minecraft_id))
    if status == True:
        # Completed, now remove from database.
        mc_database.delete(telegram_id)
        update.message.reply_text("Completed! We have just deleted your account from the whitelist of our server. We hope to see you again.")
        mc_logging.log_delete_from_whitelist(telegram_id, minecraft_id)
        return True
    elif status == False:
        # User doesn't exist
        update.message.reply_text("We cannot verify the existence of your account.\nPlease check the username you have submitted.")
        mc_logging.log_invalid_user(telegram_id, minecraft_id)
        return False
    
def show(update: Update, context: CallbackContext) -> None:
    telegram_id = update.message.from_user.id
    telegram_id = str(telegram_id)
    if mc_database.check_not_exist_by_telegram_id(telegram_id):
        update.message.reply_text("You never registered an account.")
        mc_logging.log_show_themselves_but_not_exist(telegram_id)
        return False
    # Fetch the player ID with Telegram ID
    # The value should be a tuple
    minecraft_id = mc_database.fetch_minecraft_id_by_telegram_id(telegram_id)
    update.message.reply_text("Telegram account " + str(telegram_id) + " currently tied with Minecraft account " + str(minecraft_id))
    mc_logging.log_show_themselves(telegram_id, minecraft_id)
    return True

def main():
    # Initialize the database if not exists
    print("Initializing database...")
    mc_database.initialize()

    # Set up the bot
    print("Setting up the bot...")
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("remove", remove))
    dp.add_handler(CommandHandler("show", show))

    # Start looping
    print("Starting to loop...")
    mc_logging.log_botstart()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()