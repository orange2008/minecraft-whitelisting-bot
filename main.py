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

# Read bot token
with open("config.json") as f:
    conf = json.load(f)
TOKEN = conf['bot_token']

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Welcome to Prism's Minecraft Server. \nThe Server has whitelist turned on, so you will need to register your Minecraft account using this bot.\nNote that the Telegram account will be tied to your Minecraft account.\nYou are responsible for everything you are going to do in the server and we reserve the right to bring proceedings in the courts of the Hong Kong Special Administrative Region.")

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
        return False
    update.message.reply_text("You are about to register your Minecraft account with playerID " + minecraft_id + " on our server.")
    # Some async stuff, because sync doesn't work...
    tasklist = [mc_whitelist.add_to_whitelist(minecraft_id)]
    # Deprecated, because something weird could happen.
    # loops = asyncio.get_event_loop()
    try:
        loops = asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            loops = asyncio.new_event_loop()
            asyncio.set_event_loop(loops)
    status = loops.run_until_complete(asyncio.wait(tasklist))
    if status:
        # Completed, now add to database.
        minecraft_uuid = mc_getuuid.getuuid(minecraft_id)
        mc_database.insert(telegram_id, minecraft_id, minecraft_uuid)
        update.message.reply_text("Completed! We have just added your account to the whitelist. Launch your game and enjoy!")
        return True
    else:
        # User doesn't exist
        update.message.reply_text("We cannot verify the existence of your account.\nPlease check the username you have submitted.")
        return False
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

    # Start looping
    print("Starting to loop...")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()