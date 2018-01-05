# from tesserocr import PyTessBaseAPI
import pkg_resources
from tesserocr import PyTessBaseAPI
from urllib import request
import twitter
from bittrex.bittrex import Bittrex
import re
from detection.bittrex_detector import BittrexService

TRACKED_USER = '@haydart_'
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


def track_that_mcafee_bastard():
    # use a generator that yields one status at a time
    print('Listening for incoming tweets')
    for line in twitter_api.GetStreamFilter(follow=TRACKED_USER_ID, languages=LANGUAGES):
        process_tweet_if_written_by_mcafee(line)


def process_tweet_if_written_by_mcafee(tweet):
    # filter out all retweets & replies
    if tweet['user']['screen_name'] == TRACKED_USER and 'retweeted_status' not in tweet.keys() and \
            not tweet['text'].startswith('RT'):
        print("")
        print(TRACKED_USER, 'AUTHORED TWEET')
        print(tweet)
        print("")
        analyse_ocr(tweet['extended_entities']['media'][0]['media_url'])
        # expecting to have the promoted coin as plain text embedded in picture


def analyse_ocr(url):
    with PyTessBaseAPI() as api:
        print(url)
        request.urlretrieve(url, 'mcafeecoin.jpg')
        api.SetImageFile('mcafeecoin.jpg')
        print(api.GetUTF8Text())
        print(api.AllWordConfidences())


# process_tweet_if_written_by_mcafee(
#     {'created_at': 'Mon Jan 01 15:03:12 +0000 2018', 'id': 947845669213147136, 'id_str': '947845669213147136',
#      'text': 'Coin of the week; https://t.co/ZWISkUX6Ok', 'display_text_range': [0, 17],
#      'source': '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>',
#      'truncated': False, 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None,
#      'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None,
#      'user': {'id': 961445378, 'id_str': '961445378', 'name': 'John McAfee', 'screen_name': 'officialmcafee',
#               'location': 'House McAfee', 'url': None,
#               'description': 'Tech Pioneer, Chief Cybersecurity Visionary of MGT. Trustee - Keep This Bastard Alive fund.',
#               'translator_type': 'none', 'protected': False, 'verified': True, 'followers_count': 570417,
#               'friends_count': 12324, 'listed_count': 4454, 'favourites_count': 12682, 'statuses_count': 8452,
#               'created_at': 'Wed Nov 21 00:03:03 +0000 2012', 'utc_offset': -28800,
#               'time_zone': 'Pacific Time (US & Canada)', 'geo_enabled': False, 'lang': 'en',
#               'contributors_enabled': False, 'is_translator': False, 'profile_background_color': 'FFFFFF',
#               'profile_background_image_url': 'http://pbs.twimg.com/profile_background_images/463138421511168000/3E83MZd8.png',
#               'profile_background_image_url_https': 'https://pbs.twimg.com/profile_background_images/463138421511168000/3E83MZd8.png',
#               'profile_background_tile': False, 'profile_link_color': 'FAB81E',
#               'profile_sidebar_border_color': '000000', 'profile_sidebar_fill_color': 'C0DFEC',
#               'profile_text_color': '088253', 'profile_use_background_image': True,
#               'profile_image_url': 'http://pbs.twimg.com/profile_images/722878117967036416/2MOt13No_normal.jpg',
#               'profile_image_url_https': 'https://pbs.twimg.com/profile_images/722878117967036416/2MOt13No_normal.jpg',
#               'profile_banner_url': 'https://pbs.twimg.com/profile_banners/961445378/1466659018',
#               'default_profile': False, 'default_profile_image': False, 'following': None, 'follow_request_sent': None,
#               'notifications': None}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None,
#      'is_quote_status': False, 'quote_count': 0, 'reply_count': 0, 'retweet_count': 0, 'favorite_count': 0,
#      'entities': {'hashtags': [], 'urls': [], 'user_mentions': [], 'symbols': [], 'media': [
#          {'id': 947845658886549504, 'id_str': '947845658886549504', 'indices': [18, 41], 'media_url': '.',
#           'media_url_https': 'https://pbs.twimg.com/media/DSdsmtfUMAAtWLx.jpg', 'url': 'https://t.co/ZWISkUX6Ok',
#           'display_url': 'pic.twitter.com/ZWISkUX6Ok',
#           'expanded_url': 'https://twitter.com/officialmcafee/status/947845669213147136/photo/1', 'type': 'photo',
#           'sizes': {'thumb': {'w': 150, 'h': 150, 'resize': 'crop'}, 'medium': {'w': 1080, 'h': 962, 'resize': 'fit'},
#                     'large': {'w': 1080, 'h': 962, 'resize': 'fit'}, 'small': {'w': 680, 'h': 606, 'resize': 'fit'}}}]},
#      'extended_entities': {'media': [{'id': 947845658886549504, 'id_str': '947845658886549504', 'indices': [18, 41],
#                                       'media_url': 'http://pbs.twimg.com/media/DSdsmtfUMAAtWLx.jpg',
#                                       'media_url_https': 'https://pbs.twimg.com/media/DSdsmtfUMAAtWLx.jpg',
#                                       'url': 'https://t.co/ZWISkUX6Ok', 'display_url': 'pic.twitter.com/ZWISkUX6Ok',
#                                       'expanded_url': 'https://twitter.com/officialmcafee/status/947845669213147136/photo/1',
#                                       'type': 'photo', 'sizes': {'thumb': {'w': 150, 'h': 150, 'resize': 'crop'},
#                                                                  'medium': {'w': 1080, 'h': 962, 'resize': 'fit'},
#                                                                  'large': {'w': 1080, 'h': 962, 'resize': 'fit'},
#                                                                  'small': {'w': 680, 'h': 606, 'resize': 'fit'}}}]},
#      'favorited': False, 'retweeted': False, 'possibly_sensitive': False, 'filter_level': 'low', 'lang': 'en',
#      'timestamp_ms': '1514818992318'})
