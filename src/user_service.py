import os
import requests


def get_user(user_id):
    if not user_id:
        raise ValueError("user_id is required")

    api_url = os.getenv("API_URL")

    response = requests.get(
        f"{api_url}/users/{user_id}",
        timeout=10
    )

    response.raise_for_status()

    return response.json()
