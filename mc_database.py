#!/usr/bin/python3
import sqlite3
import datetime

# DATABASE: telegram_id TEXT | minecraft_id TEXT | minecraft_uuid TEXT | timestamp TEXT

def initialize():
    # Note that the initialization only works when the database doesn't exist.
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (telegram_id TEXT, minecraft_id TEXT, minecraft_uuid TEXT, timestamp TEXT)''')
    conn.close()

def timestamp():
    return datetime.datetime.now().astimezone().isoformat()

def insert(telegram_id, minecraft_id, minecraft_uuid):
    telegram_id = str(telegram_id)
    minecraft_id = str(minecraft_id)
    minecraft_uuid = str(minecraft_uuid)
    ts = timestamp()
    # Check existence
    if check_not_exist_by_telegram_id(telegram_id):
        pass
    else:
        return False
    # Connect to database
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (telegram_id, minecraft_id, minecraft_uuid, timestamp) VALUES (?, ?, ?, ?)", (telegram_id, minecraft_id, minecraft_uuid, ts,))
    # Save changes
    conn.commit()
    conn.close()
    return True

def delete(telegram_id):
    telegram_id = str(telegram_id)
    # Check existence
    if check_not_exist_by_telegram_id(telegram_id):
        pass
    else:
        return False
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE telegram_id=?", (telegram_id,))
    conn.commit()
    conn.close()
    return True

def check_not_exist_by_telegram_id(telegram_id):
    telegram_id = str(telegram_id)
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM users WHERE telegram_id=?", (telegram_id,))
    if cursor.fetchone():
        # User exists
        conn.close()
        return False
    else:
        conn.close()
        return True

def check_not_exist_by_minecraft_id(minecraft_id):
    minecraft_id = str(minecraft_id)
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT minecraft_id from users WHERE minecraft_id=?", (minecraft_id,))
    if cursor.fetchone():
        # User exists
        conn.close()
        return False
    else:
        conn.close()
        return True