from getpass import getpass

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import UpdateNewChannelMessage
import numpy as np
import cv2.text as cv_ext
import cv2 as cv_core

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
            code = input('Enter the auth code: ')
            try:
                code_ok = client.sign_in(user_phone, code)
            except SessionPasswordNeededError:
                password = getpass('Two step verification enabled. Please enter your password: ')
                code_ok = client.sign_in(password=password)
    print('Client initialized')

    client.add_update_handler(update_handler)

    img = cv_core.imread("image1.jpg")
    text_spotter = cv_ext.TextDetectorCNN_create("textbox.prototxt", "TextBoxes_icdar13.caffemodel")
    rects, out_probs = text_spotter.detect(img)
    vis = img.copy()
    threshold = 0.6

    for r in range(np.shape(rects)[0]):
        if out_probs[r] > threshold:
            rect = rects[r]
            cv_core.rectangle(vis, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 2)

    cv_core.imshow("Text detection result", vis)


def update_handler(update):
    if isinstance(update, UpdateNewChannelMessage):
        print(update)


if __name__ == '__main__':
    initialize_client()
