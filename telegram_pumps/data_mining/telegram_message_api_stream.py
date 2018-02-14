from getpass import getpass

import psycopg2
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import UpdateNewChannelMessage

from common.database.database_connection import create_db_connection
from telegram_pumps.data_mining.launch_mode_provider import is_auth_code_available, fetch_auth_code_from_db, \
    save_session_file, save_phone_code_hash, fetch_phone_code_hash_from_db
from telegram_pumps.data_mining.message_handler import MessagesHandler

user_phone = '+048698393574'
messages_handler = MessagesHandler()


def _initialize_client():
    client = TelegramClient(
        'telegram',
        136572,
        '4c32af0a85f96a579d7e6f9f59fd7a77',
        proxy=None,
        update_workers=4
    )

    print('INFO: Connecting to Telegram Servers...', end='', flush=True)
    client.connect()

    if not client.is_user_authorized():
        print('Unauthorized user')

        if is_auth_code_available():
            code_ok = False
            while not code_ok:
                auth_code = fetch_auth_code_from_db()
                phone_code_hash = fetch_phone_code_hash_from_db()
                print(phone_code_hash)
                try:
                    code_ok = client.sign_in(user_phone, auth_code, phone_code_hash=phone_code_hash)
                except SessionPasswordNeededError:
                    password = getpass('Two step verification enabled. Please enter your password: ')
                    code_ok = client.sign_in(password=password)

            save_session_file()
        else:
            resend_code_request = client.send_code_request(user_phone)
            phone_code_hash = resend_code_request.phone_code_hash
            print('Phone code hash', phone_code_hash)
            save_phone_code_hash(phone_code_hash)
            print('A fresh auth code has been sent. Please update the value in db and deploy')

            # launch an infinite loop to prevent Heroku from restarting the script resulting in a telegram API ban
            _launch_infinite_loop()

    print('Client initialized')
    client.add_update_handler(_update_handler)

    _launch_infinite_loop()


def _launch_infinite_loop():
    while True:
        pass


def _update_handler(update):
    if isinstance(update, UpdateNewChannelMessage):
        messages_handler.handle_data_updates(update.message)


if __name__ == '__main__':
    _initialize_client()
