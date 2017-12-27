import requests


response = requests.get(
    "https://wordsapiv1.p.mashape.com/words/bump/definitions",
    headers={
        "X-Mashape-Key": "uULjTmQjUXmshKdlmT1F3UtG9GCqp1wtv5djsnA4bns4s0ORL4",
        "Accept": "application/json"
    }
)
# using english words API to punish the coin names that are normal words
# WARNING: no more than 2500 requests/day
print(response.json())

def fetch_word_definitions_count():

