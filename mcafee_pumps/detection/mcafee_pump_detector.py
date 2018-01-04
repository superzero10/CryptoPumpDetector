# from tesserocr import PyTessBaseAPI
from tesserocr import PyTessBaseAPI
from urllib import request
import twitter
from bittrex.bittrex import Bittrex
import re
from detection.bittrex_detector import BittrexService

TRACKED_USER = ['@officialmcafee']
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


def process_tweet_if_written_by_mcafee(tweet):
    # filter out all retweets & replies
    if tweet['user']['screen_name'] == "officialmcafee" and 'retweeted_status' not in tweet.keys() and not tweet[
        'text'].startswith('RT'):
        print("")
        print("MCAFEE AUTHORED TWEET")
        print(tweet)
        print("")

        # expecting to have the promoted coin as plain text embedded in picture


def analyse_ocr():
    with PyTessBaseAPI() as api:
        request.urlretrieve("http://pbs.twimg.com/media/DSdsmtfUMAAtWLx.jpg", "mcafee.jpg")
        api.SetImageFile('mcafee.jpg')
        print(api.GetUTF8Text())
        print(api.AllWordConfidences())


# analyse_ocr()
# process_tweet_if_written_by_mcafee({'created_at': 'Wed Jan 03 23:33:42 +0000 2018', 'id': 948698917633495040, 'id_str': '948698917633495040', 'text': 'RT @BobsRepair: @BobsRepair is excited to announce Brandon Kite as our new CTO. He was previously the Lead Developer at Dragonchain and the…', 'source': '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', 'truncated': False, 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 961445378, 'id_str': '961445378', 'name': 'John McAfee', 'screen_name': 'officialmcafee', 'location': 'House McAfee', 'url': None, 'description': 'Tech Pioneer, Chief Cybersecurity Visionary of MGT. Trustee - Keep This Bastard Alive fund.', 'translator_type': 'none', 'protected': False, 'verified': True, 'followers_count': 596375, 'friends_count': 12325, 'listed_count': 4686, 'favourites_count': 12655, 'statuses_count': 8458, 'created_at': 'Wed Nov 21 00:03:03 +0000 2012', 'utc_offset': -28800, 'time_zone': 'Pacific Time (US & Canada)', 'geo_enabled': False, 'lang': 'en', 'contributors_enabled': False, 'is_translator': False, 'profile_background_color': 'FFFFFF', 'profile_background_image_url': 'http://pbs.twimg.com/profile_background_images/463138421511168000/3E83MZd8.png', 'profile_background_image_url_https': 'https://pbs.twimg.com/profile_background_images/463138421511168000/3E83MZd8.png', 'profile_background_tile': False, 'profile_link_color': 'FAB81E', 'profile_sidebar_border_color': '000000', 'profile_sidebar_fill_color': 'C0DFEC', 'profile_text_color': '088253', 'profile_use_background_image': True, 'profile_image_url': 'http://pbs.twimg.com/profile_images/722878117967036416/2MOt13No_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/722878117967036416/2MOt13No_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/961445378/1466659018', 'default_profile': False, 'default_profile_image': False, 'following': None, 'follow_request_sent': None, 'notifications': None}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'retweeted_status': {'created_at': 'Tue Jan 02 21:03:19 +0000 2018', 'id': 948298685913288705, 'id_str': '948298685913288705', 'text': '@BobsRepair is excited to announce Brandon Kite as our new CTO. He was previously the Lead Developer at Dragonchain… https://t.co/HB3ldKjp3a', 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'truncated': True, 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': 901920700583129088, 'in_reply_to_user_id_str': '901920700583129088', 'in_reply_to_screen_name': 'BobsRepair', 'user': {'id': 901920700583129088, 'id_str': '901920700583129088', 'name': 'BobsRepair', 'screen_name': 'BobsRepair', 'location': 'Las Vegas, NV', 'url': 'http://www.BobsRepair.com', 'description': 'First brick & mortar service to hold a token offering. Trusted transactions between home owners & repair contractors. #ICO #cryptocurrency #BTC #ETH #blockchain', 'translator_type': 'none', 'protected': False, 'verified': False, 'followers_count': 7169, 'friends_count': 2261, 'listed_count': 21, 'favourites_count': 1226, 'statuses_count': 243, 'created_at': 'Sun Aug 27 21:33:46 +0000 2017', 'utc_offset': -28800, 'time_zone': 'Pacific Time (US & Canada)', 'geo_enabled': True, 'lang': 'en', 'contributors_enabled': False, 'is_translator': False, 'profile_background_color': 'F5F8FA', 'profile_background_image_url': '', 'profile_background_image_url_https': '', 'profile_background_tile': False, 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'profile_image_url': 'http://pbs.twimg.com/profile_images/920709720960221184/L7JRGrTk_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/920709720960221184/L7JRGrTk_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/901920700583129088/1507888993', 'default_profile': True, 'default_profile_image': False, 'following': None, 'follow_request_sent': None, 'notifications': None}, 'geo': None, 'coordinates': None, 'place': {'id': '5c2b5e46ab891f07', 'url': 'https://api.twitter.com/1.1/geo/id/5c2b5e46ab891f07.json', 'place_type': 'city', 'name': 'Las Vegas', 'full_name': 'Las Vegas, NV', 'country_code': 'US', 'country': 'United States', 'bounding_box': {'type': 'Polygon', 'coordinates': [[[-115.384091, 36.129459], [-115.384091, 36.336371], [-115.062159, 36.336371], [-115.062159, 36.129459]]]}, 'attributes': {}}, 'contributors': None, 'is_quote_status': False, 'extended_tweet': {'full_text': '@BobsRepair is excited to announce Brandon Kite as our new CTO. He was previously the Lead Developer at Dragonchain and the Senior Software Engineer at The Walt Disney Company. He will be in charge of creating the BOB Application Ecosystem. https://t.co/gxHMgvX5wW', 'display_text_range': [0, 264], 'entities': {'hashtags': [], 'urls': [{'url': 'https://t.co/gxHMgvX5wW', 'expanded_url': 'https://bobsrepair.com/#news', 'display_url': 'bobsrepair.com/#news', 'indices': [241, 264]}], 'user_mentions': [{'screen_name': 'BobsRepair', 'name': 'BobsRepair', 'id': 901920700583129088, 'id_str': '901920700583129088', 'indices': [0, 11]}], 'symbols': []}}, 'quote_count': 11, 'reply_count': 0, 'retweet_count': 219, 'favorite_count': 217, 'entities': {'hashtags': [], 'urls': [{'url': 'https://t.co/HB3ldKjp3a', 'expanded_url': 'https://twitter.com/i/web/status/948298685913288705', 'display_url': 'twitter.com/i/web/status/9…', 'indices': [117, 140]}], 'user_mentions': [{'screen_name': 'BobsRepair', 'name': 'BobsRepair', 'id': 901920700583129088, 'id_str': '901920700583129088', 'indices': [0, 11]}], 'symbols': []}, 'favorited': False, 'retweeted': False, 'possibly_sensitive': False, 'filter_level': 'low', 'lang': 'en'}, 'is_quote_status': False, 'quote_count': 0, 'reply_count': 0, 'retweet_count': 0, 'favorite_count': 0, 'entities': {'hashtags': [], 'urls': [], 'user_mentions': [{'screen_name': 'BobsRepair', 'name': 'BobsRepair', 'id': 901920700583129088, 'id_str': '901920700583129088', 'indices': [3, 14]}, {'screen_name': 'BobsRepair', 'name': 'BobsRepair', 'id': 901920700583129088, 'id_str': '901920700583129088', 'indices': [16, 27]}], 'symbols': []}, 'favorited': False, 'retweeted': False, 'filter_level': 'low', 'lang': 'en', 'timestamp_ms': '1515022422594'})
analyse_ocr()
