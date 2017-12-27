import requests


# Use english words API to punish the coin names that are normal words & could have been used not relating to coin name
# Heuristic: the more the existing word definitions, the higher the punishment gets
# WARNING: no more than 2500 requests/day

def fetch_word_definitions_count(word):
    response = requests.get(
        "https://wordsapiv1.p.mashape.com/words/" + word + "/definitions",
        headers={
            "X-Mashape-Key": "uULjTmQjUXmshKdlmT1F3UtG9GCqp1wtv5djsnA4bns4s0ORL4",
            "Accept": "application/json"
        }
    )
    result = 0
    try:
        result = len(response.json()['definitions'])
    finally:
        return result
