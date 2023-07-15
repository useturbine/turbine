from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.models import User
from config import config

import base64

class PastThreads:
    def __init__(self):
        self.service = None

    def get_by_email(self, user_email: str):
        user = User.get(User.email == user_email)
        self.service = build(
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
            for thread in self.service.users().threads().list(userId="me", includeSpamTrash=False,
                                                              q="from:sumit.ghosh32@gmail.com is:read").execute()[
                "threads"]
        ]

        msg_list = []

        for thread_id in thread_ids:
            msg = self.parse_email_content(thread_id)
            msg_list.extend(msg)

        return msg_list

    @staticmethod
    def get_header_value(headers, name):
        for header in headers:
            if header["name"] == name:
                return header["value"]
        return None

    def parse_email_content(self, thread_id):
        thread = self.service.users().threads().get(userId="me", id=thread_id).execute()
        messages = thread["messages"]

        plain_messages = []
        for message in messages:
            payload = message["payload"]
            headers = payload["headers"]

            subject = PastThreads.get_header_value(headers, "Subject")
            parts = payload.get("parts", [])

            for part in parts:
                if part["mimeType"] != "text/plain":
                    continue

                data = part.get("body", {}).get("data", "")
                if not data:
                    # if "data" is not present, try getting the plaintext from "body" directly
                    text = part.get("body", "").get("text", "")
                    plain_messages.append({"subject": subject, "text": text})
                    continue

                text = base64.urlsafe_b64decode(data).decode("utf-8")
                plain_messages.append({"subject": subject, "text": text})

        return plain_messages
