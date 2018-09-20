import os
from datetime import datetime

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import UpdateNewChannelMessage

from telegram_pumps.print_cwd_files import print_directory_files


class TelegramApiClient:
    _user_phone = os.environ.get('USER_PHONE')
    _message_handler = None

    def __init__(self, message_handler):
        self._message_handler = message_handler  # function taking telegram update as argument
        self.__initialize_client()

    def __initialize_client(self):
        print_directory_files()
        saved_session = self.__read_or_create_session()
        client = self.__create_client_with_session(saved_session)

        print(datetime.time(datetime.now()), 'INFO: Connecting to Telegram Servers...', end='', flush=True)
        client.connect()

        print(datetime.time(datetime.now()), 'Client initialized, waiting for updates.')
        client.add_event_handler(self.__update_handler)

        with client.start():
            self.__write_session_file(client)
            print('(Press Ctrl+C to stop this)')
            client.run_until_disconnected()

    def __read_or_create_session(self):
        session_file = self.__read_session_file()

        if session_file is None:
            # create a new session (mobile auth code required)
            return StringSession()
        else:
            # recreate session from existing file
            return StringSession(session_file)

    def __read_session_file(self):
        try:
            with open('session.txt', 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def __create_client_with_session(self, session):
        return TelegramClient(
            session,
            api_id=os.environ.get('API_ID'),
            api_hash=os.environ.get('API_HASH'),
            proxy=None
        )

    async def __update_handler(self, update):
        if isinstance(update, UpdateNewChannelMessage):
            print(update)
            try:
                self._message_handler(update.message)  # whole Message object
            except RuntimeError as error:
                print(error)

    def __write_session_file(self, client):
        with open('session.txt', 'w') as file:
            saved_session_string = client.session.save()
            file.write(saved_session_string)
            print(saved_session_string)
