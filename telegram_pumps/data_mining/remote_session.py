import requests


def retrieve_remote_session():
    with open("login.session", 'wb') as f:
        response = requests.get("https://raw.githubusercontent.com/Haydart/PDsession/master/telegram_pumps"
                                "/data_mining/login.session", verify=False)
        print(response.content)
        f.write(response.content)

