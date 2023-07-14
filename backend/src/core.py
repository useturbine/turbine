from pprint import pprint


def get_past_threads(service):
    threads = (
        service.users().threads().list(userId="me", includeSpamTrash=False).execute()
    )
    thread_details = [
        service.users().threads().get(userId="me", id=thread["id"]).execute()
        for thread in threads["threads"]
    ]
    pprint(thread_details)
