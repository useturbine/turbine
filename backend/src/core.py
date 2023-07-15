from pprint import pprint
from src.models import User
from google.oauth2.credentials import Credentials
from oauth2client.client import OAuth2Credentials
from googleapiclient.discovery import build
from config import config


def get_past_threads(user_email: str):
    user = User.get(User.email == user_email)
    service = build(
        "gmail",
        "v1",
        credentials=Credentials(
            token=user.access_token,
            refresh_token=user.refresh_token,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            client_id=config.google.client_id,
            client_secret=config.google.client_secret,
            token_uri="https://oauth2.googleapis.com/token",
        ),
    )

    thread_ids = [
        thread["id"]
        for thread in service.users()
        .threads()
        .list(userId="me", includeSpamTrash=False, q="from:ankit03june@gmail.com")
        .execute()["threads"]
    ]
    print(thread_ids)

    message = (
        service.users()
        .threads()
        .get(userId="me", id=thread_ids[0])
        .execute()["messages"][0]
    )
    # print(message)

    # thread_details = [
    #     service.users().threads().get(userId="me", id=thread["id"]).execute()
    #     for thread in threads["threads"]
    # ]
    # pprint(thread_details)
