from getpass import getpass

import sys
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from telegram_pumps.data_mining.launch_mode_provider import is_auth_code_available, obtain_auth_code_from_db

user_phone = '+048698393574'


def initialize_client():
    client = TelegramClient(
        'examplesession',
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
                auth_code = obtain_auth_code_from_db()
                try:
                    code_ok = client.sign_in(user_phone, auth_code)
                except SessionPasswordNeededError:
                    password = getpass('Two step verification enabled. Please enter your password: ')
                    code_ok = client.sign_in(password=password)
        else:
            client.send_code_request(user_phone)
            print('A fresh auth code has been sent. Please update the value in db and deploy')
            sys.exit()

    print('Client initialized')
    client.add_update_handler(update_handler)

    while True:
        pass


def update_handler(update):
    print(update)


if __name__ == '__main__':
    initialize_client()
