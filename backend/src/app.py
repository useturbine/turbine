from flask import Flask, url_for, redirect
from authlib.integrations.flask_client import OAuth
from config import config
from pprint import pprint
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


app = Flask(__name__)
app.secret_key = config.app.secret_key

oauth = OAuth(app)


@app.route("/google/")
def google():
    oauth.register(
        name="google",
        client_id=config.google.client_id,
        client_secret=config.google.client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile https://www.googleapis.com/auth/gmail.readonly"
        },
    )
    redirect_uri = url_for("google_auth", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/google/auth/")
def google_auth():
    token = oauth.google.authorize_access_token()
    pprint(token)

    service = build(
        "gmail",
        "v1",
        credentials=Credentials(token=token["access_token"], scopes=token["scope"]),
    )
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
        print("No labels found.")
        return
    print("Labels:")
    for label in labels:
        print(label["name"])

    return redirect("/")


if __name__ == "__main__":
    app.run()
