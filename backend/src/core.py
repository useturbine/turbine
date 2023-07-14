from pprint import pprint
from src.models import User
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_past_threads(user_email: str):
    user = User.get(User.email == user_email)
    service = build(
        "gmail",
        "v1",
        credentials=Credentials(
            token=user.access_token,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        ),
    )

    thread_ids = [
        thread["id"]
        for thread in service.users()
        .threads()
        .list(userId="me", includeSpamTrash=False)
        .execute()
    ]
    print(thread_ids)

    # thread_details = [
    #     service.users().threads().get(userId="me", id=thread["id"]).execute()
    #     for thread in threads["threads"]
    # ]
    # pprint(thread_details)
