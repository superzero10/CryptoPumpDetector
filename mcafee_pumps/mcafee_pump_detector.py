import json
import sys
from tesserocr import PyTessBaseAPI

import tesserocr
import twitter
from detection.bittrex_detector import BittrexService
from bittrex.bittrex import Bittrex

TRACKED_USERS = ['@officialmcafee']
LANGUAGES = ['en']
my_bittrex = Bittrex("a915c64c2fae4387ae569f0253ff5d67", "87ec1df1a1774886a342e26dcfdb9038")

active_bittrex_pairs = BittrexService().fetch_active_btc_pairs()
bittrex_coins = list(map(lambda x: x[4:], active_bittrex_pairs))
bittrex_coins = bittrex_coins + list(map(lambda x: x.lower(), bittrex_coins)) + list(map(lambda x: x.capitalize(), bittrex_coins))
print(bittrex_coins)

with PyTessBaseAPI() as api:
    api.SetImageFile('ocr_image.png')
    print(api.GetUTF8Text())
    print(api.AllWordConfidences())

print(tesserocr.file_to_text('ocr_image.png'))


def analyse_ocr(tweet):
    pass


def analyse_tweet(tweet):
    print(tweet)
    if tweet['user']['screen_name'] == "officialmcafee":
        print("WE GOT A PUMP")
        analyse_ocr(tweet)


def track_that_mcafee_bastard():
    api = twitter.Api(consumer_key='TjtC3Moxczg62gsMYNzrxGtQ3',
                      consumer_secret='rObL9LQu7pH0iU1DmvRvYiNpwzqBKtHQfWLJxBbuEfyvroAxB6',
                      access_token_key='913148816668454912-ir0ibXXXO0h2NU4PZhYIPm42ZbtNflf',
                      access_token_secret='hyTdLdsIGHaOMnPVQIaHEr3KCeThW4hlPK3BXTUkKthd6')

    statuses = api.GetUserTimeline(screen_name='@officialmcafee')
    print(statuses[0])
    #
    # print(api.VerifyCredentials())
    # api.GetStreamFilter will return a generator that yields one status
    # message (i.e., Tweet) at a time as a JSON dictionary.
    for line in api.GetStreamFilter(track=TRACKED_USERS, languages=LANGUAGES):
        print(line)
        analyse_tweet(line)
