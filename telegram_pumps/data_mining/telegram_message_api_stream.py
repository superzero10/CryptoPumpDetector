import os
from datetime import datetime

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import UpdateNewChannelMessage

from telegram_pumps.data_mining.message_processor import MessageProcessor
from telegram_pumps.print_cwd_files import print_directory_files

user_phone = os.environ.get('USER_PHONE')
messages_handler = MessageProcessor()


def _initialize_client():
    print_directory_files()
    client = create_client_with_session(read_session_file())

    print(datetime.time(datetime.now()), 'INFO: Connecting to Telegram Servers...', end='', flush=True)
    client.connect()

    print(datetime.time(datetime.now()), 'Client initialized, waiting for updates.')
    client.add_event_handler(_update_handler)

    with client.start():
        write_session_file(client)
        print('(Press Ctrl+C to stop this)')
        client.run_until_disconnected()


async def _update_handler(update):
    print(update)
    if isinstance(update, UpdateNewChannelMessage):
        messages_handler.handle_channel_updates(update.message)  # whole Message object


def read_session_file():
    try:
        with open('session.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None


def create_client_with_session(session):
    if session is None:
        # create a new session (mobile auth code required)
        string_session = StringSession()
    else:
        # recreate session from existing file
        string_session = StringSession(session)

    return TelegramClient(
        string_session,
        api_id=os.environ.get('API_ID'),
        api_hash=os.environ.get('API_HASH'),
        proxy=None
    )


def write_session_file(client):
    with open('session.txt', 'w') as file:
        saved_session_string = client.session.save()
        file.write(saved_session_string)
        print(saved_session_string)


if __name__ == '__main__':
    _initialize_client()
