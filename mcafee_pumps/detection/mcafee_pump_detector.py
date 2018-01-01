# from tesserocr import PyTessBaseAPI
import twitter
from bittrex.bittrex import Bittrex
import re
from detection.bittrex_detector import BittrexService

TRACKED_USER = ['@haydart_']
LANGUAGES = ['en', 'pl']
alphanumerics_pattern = re.compile('([^\s\w]|_)+')

my_bittrex = Bittrex("a915c64c2fae4387ae569f0253ff5d67", "87ec1df1a1774886a342e26dcfdb9038")

active_bittrex_pairs = BittrexService().fetch_active_btc_pairs()
twitter_api = twitter.Api(consumer_key='TjtC3Moxczg62gsMYNzrxGtQ3',
                          consumer_secret='rObL9LQu7pH0iU1DmvRvYiNpwzqBKtHQfWLJxBbuEfyvroAxB6',
                          access_token_key='913148816668454912-ir0ibXXXO0h2NU4PZhYIPm42ZbtNflf',
                          access_token_secret='hyTdLdsIGHaOMnPVQIaHEr3KCeThW4hlPK3BXTUkKthd6')


def track_that_mcafee_bastard():
    # use a generator that yields one status at a time
    print("Listening for incoming tweets")
    for line in twitter_api.GetStreamFilter(follow=['961445378'], languages=LANGUAGES):
        # print(line)
        process_tweet_if_written_by_mcafee(line)

    for line in twitter_api.GetUserStream(withuser='961445378'):
        print("ASD", line)
        # process_tweet_if_written_by_mcafee(line)


def process_tweet_if_written_by_mcafee(tweet):
    # filter out all retweets & replies
    if tweet['user']['screen_name'] == "officialmcafee":
        print("")
        print("MCAFEE AUTHORED TWEET")
        print(tweet)
        print("")

        # expecting to have the promoted coin as plain text embedded in picture
        # analyse_ocr(tweet)
#
#
# def analyse_ocr(tweet):
#     with PyTessBaseAPI() as api:
#         api.SetImageFile('ocr_samples/ocr_image.png')
#         print(api.GetUTF8Text())
#         print(api.AllWordConfidences())

