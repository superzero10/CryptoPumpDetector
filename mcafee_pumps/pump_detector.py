import json
import twitter
from detection.bittrex_detector import BittrexService

TRACKED_USERS = ['@officialmcafee']
LANGUAGES = ['en']

last_tweet_text = ''
active_bittrex_pairs = BittrexService().fetch_active_btc_pairs()
truncator = lambda x: x[4:]
bittrex_coins = list(map(truncator, active_bittrex_pairs))
print(bittrex_coins)


def analyseTweet(text):
    pass


def track_that_mcafee_bastard():
    api = twitter.Api(consumer_key='TjtC3Moxczg62gsMYNzrxGtQ3',
                      consumer_secret='rObL9LQu7pH0iU1DmvRvYiNpwzqBKtHQfWLJxBbuEfyvroAxB6',
                      access_token_key='913148816668454912-ir0ibXXXO0h2NU4PZhYIPm42ZbtNflf',
                      access_token_secret='hyTdLdsIGHaOMnPVQIaHEr3KCeThW4hlPK3BXTUkKthd6')

    # print(api.VerifyCredentials())
    # # api.GetStreamFilter will return a generator that yields one status
    # # message (i.e., Tweet) at a time as a JSON dictionary.
    # for line in api.GetStreamFilter(track=TRACKED_USERS, languages=LANGUAGES):
    #     print(json.dumps(line))

    statuses = api.GetUserTimeline(screen_name='@officialmcafee')
    print(statuses[0].text)
    analyseTweet(statuses[0].text)
