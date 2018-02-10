from getpass import getpass

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import UpdateNewChannelMessage

from telegram_pumps.data_mining.launch_mode_provider import is_auth_code_available, fetch_auth_code_from_db
from telegram_pumps.data_mining.telegram_data_filter import handle_data_updates

user_phone = '+048698393574'


def _initialize_client():
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
                auth_code = fetch_auth_code_from_db()
                try:
                    code_ok = client.sign_in(user_phone, auth_code, phone_code_hash='87beda67ec8bc04b5d')
                    print(auth_code)
                except SessionPasswordNeededError:
                    password = getpass('Two step verification enabled. Please enter your password: ')
                    code_ok = client.sign_in(password=password)
        else:
            phone_code_hash = client.send_code_request(user_phone)
            print(phone_code_hash)
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
        handle_data_updates(update.message)


if __name__ == '__main__':
    _initialize_client()
