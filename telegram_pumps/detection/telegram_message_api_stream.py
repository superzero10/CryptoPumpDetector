from getpass import getpass
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

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
        client.send_code_request(user_phone)
        code_ok = False
        while not code_ok:
            code = open('auth_code.txt').readline()
            try:
                code_ok = client.sign_in(user_phone, code)
            except SessionPasswordNeededError:
                password = getpass('Two step verification enabled. Please enter your password: ')
                code_ok = client.sign_in(password=password)
    print('Client initialized')

    client.add_update_handler(update_handler)

    while True:
        pass


def update_handler(update):
    print(update)


if __name__ == '__main__':
    initialize_client()
