# Minecraft Whitelisting Bot
This project is used to let end-users (Minecraft players) register/remove their account from the Minecraft Server using a Telegram bot interactively.

Currently in active maintainence.

## Requirements
Python >= 3.9

## Deployment
Make sure you have Python 3 and PIP installed.

```bash
git clone https://github.com/orange2008/minecraft-whitelisting-bot.git
cd minecraft-whitelisting-bot
pip3 install -r ./requirements.txt
cp config.def.json config.json
```

Open `config.json` and fill all the blanks.

> Remember to contact [@BotFather](https://t.me/BotFather) to obtain a bot token and enable rcon on your Minecraft Server.

Then, use `./main.py` to fire up the system.

## Maintainer
Frank Ruan -- [https://frank-ruan.com](https://frank-ruan.com)