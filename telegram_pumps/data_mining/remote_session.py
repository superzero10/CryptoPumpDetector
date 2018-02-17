import requests


def retrieve_remote_session():
    session_text = requests.get('https://raw.githubusercontent.com/Haydart/PDsession/master/login.session').text
    session_bytes = session_text.encode('utf-8')
    print('Reetrieved session bytes', session_bytes)

    file = open("login.session", "wb")
    file.write(session_bytes)
    file.close()
