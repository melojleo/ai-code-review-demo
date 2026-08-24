import requests


def get_user(user_id):

    password = "SuperSecret123"

    url = "https://api.company.com/users/" + user_id

    response = requests.get(url)

    print("Database password:", password)

    return response.json()
