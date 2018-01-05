# from tesserocr import PyTessBaseAPI
import pkg_resources
from tesserocr import PyTessBaseAPI
from urllib import request
import twitter
from bittrex.bittrex import Bittrex
import re
from detection.bittrex_detector import BittrexService
from mcafee_pumps.detection.coin_dictionary import fetch_word_evaluation_dictionary

TRACKED_USER = 'haydart_'
TRACKED_USER_ID = ['913148816668454912']
LANGUAGES = ['en', 'pl']
alphanumerics_pattern = re.compile('([^\s\w]|_)+')

print('TesserOcr version:', pkg_resources.get_distribution("tesserocr").version)

my_bittrex = Bittrex("a915c64c2fae4387ae569f0253ff5d67", "87ec1df1a1774886a342e26dcfdb9038")
active_bittrex_pairs = BittrexService().fetch_active_btc_pairs()
twitter_api = twitter.Api(consumer_key='TjtC3Moxczg62gsMYNzrxGtQ3',
                          consumer_secret='rObL9LQu7pH0iU1DmvRvYiNpwzqBKtHQfWLJxBbuEfyvroAxB6',
                          access_token_key='913148816668454912-ir0ibXXXO0h2NU4PZhYIPm42ZbtNflf',
                          access_token_secret='hyTdLdsIGHaOMnPVQIaHEr3KCeThW4hlPK3BXTUkKthd6')
word_eval_dict = fetch_word_evaluation_dictionary()
print(word_eval_dict)


def track_that_mcafee_bastard():
    # use a generator that yields one status at a time
    print('Listening for incoming tweets')
    for line in twitter_api.GetStreamFilter(follow=TRACKED_USER_ID, languages=LANGUAGES):
        process_tweet_if_written_by_tracked_user(line)


def process_tweet_if_written_by_tracked_user(tweet):
    # filter out all retweets & replies
    print(tweet)
    if tweet['user']['screen_name'] == TRACKED_USER and 'retweeted_status' not in tweet.keys() and \
            not tweet['text'].startswith('RT'):
        print("")
        print(TRACKED_USER, 'AUTHORED TWEET')
        print(tweet)
        print("")
        if 'extended_entities' in tweet.keys() and 'media' in tweet['extended_entities'].keys():
            analyse_ocr(tweet['extended_entities']['media'][0]['media_url'])
            # expecting to have the promoted coin as plain text embedded in picture
        else:
            print('There was no image attached.')


def analyse_ocr(url):
    with PyTessBaseAPI() as api:
        print(url)
        request.urlretrieve(url, 'mcafeecoin.jpg')
        api.SetImageFile('mcafeecoin.jpg')
        recognized_text = api.GetUTF8Text()
        print()
        print(api.AllWordConfidences())
        extract_possible_coin_name(recognized_text)


def extract_possible_coin_name(text):
    print(text)
