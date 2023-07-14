from flask import Flask, url_for, redirect
from authlib.integrations.flask_client import OAuth
from config import config
from pprint import pprint
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from src.core import get_past_threads

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
    service = build(
        "gmail",
        "v1",
        credentials=Credentials(token=token["access_token"], scopes=token["scope"]),
    )
    get_past_threads(service)
    return redirect("/")
