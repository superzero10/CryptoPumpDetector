import os
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.types import UpdateNewChannelMessage

from telegram_pumps.data_mining.message_processor import MessageProcessor
from telegram_pumps.data_mining.remote_session import retrieve_remote_session
from telegram_pumps.print_cwd_files import print_directory_files

user_phone = os.environ.get('USER_PHONE')
messages_handler = MessageProcessor()


def _initialize_client():
    retrieve_remote_session()
    print_directory_files()

    # client = TelegramClient('login.session', os.environ["API_ID"], os.environ["API_HASH"]).start()

    client = TelegramClient(
        session='login',
        api_id=os.environ.get('API_ID'),
        api_hash=os.environ.get('API_HASH'),
        proxy=None,
        update_workers=4
    )

    print(datetime.time(datetime.now()), 'INFO: Connecting to Telegram Servers...', end='', flush=True)
    client.connect()

    if not client.is_user_authorized():
        print(datetime.time(datetime.now()), 'Unauthorized user')
    #
    #     if is_auth_code_available():
    #         code_ok = False
    #         while not code_ok:
    #             auth_code = fetch_auth_code_from_db()
    #             phone_code_hash = fetch_phone_code_hash_from_db()
    #             print(datetime.time(datetime.now()), phone_code_hash)
    #             try:
    #                 print(datetime.time(datetime.now()), 'authcode used = ', auth_code)
    #                 print(datetime.time(datetime.now()), 'codehash used = ', phone_code_hash)
    #                 code_ok = client.sign_in(user_phone, auth_code, phone_code_hash=phone_code_hash)
    #             except SessionPasswordNeededError:
    #                 password = getpass('Two step verification enabled. Please enter your password: ')
    #                 code_ok = client.sign_in(password=password)
    #
    #         save_session_file()
    #     else:
    #         resend_code_request = client.send_code_request(user_phone)
    #         phone_code_hash = resend_code_request.phone_code_hash
    #         print(datetime.time(datetime.now()), 'Phone code hash', phone_code_hash)
    #         save_phone_code_hash(phone_code_hash)
    #         print(datetime.time(datetime.now()), 'A fresh auth code has been sent. Please update the value in db and deploy')
    #
    #         # launch an infinite loop to prevent Heroku from restarting the script resulting in a telegram API ban
    #         _launch_infinite_loop()

    print(datetime.time(datetime.now()), 'Client initialized, waiting for updates.')
    client.add_update_handler(_update_handler)
    _launch_infinite_loop()


def _launch_infinite_loop():
    while True:
        pass


def _update_handler(update):
    if isinstance(update, UpdateNewChannelMessage):
        messages_handler.handle_channel_updates(update.message)  # whole Message object


if __name__ == '__main__':
    _initialize_client()
