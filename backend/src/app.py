from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from config import config
from src.models import User
from src.core import get_past_threads

app = Flask(__name__)
app.secret_key = config.app.secret_key

oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=config.google.client_id,
    client_secret=config.google.client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile https://www.googleapis.com/auth/gmail.readonly"
    },
)


@app.route("/")
def home():
    user_email = session.get("user_email")

    if not session.get("user_email"):
        return redirect(url_for("login_google"))

    user = User.get_or_none(User.email == user_email)
    get_past_threads(user.email)
    return f"Hello {user.name}!"


@app.route("/login/google/")
def login_google():
    redirect_uri = url_for("auth_google", _external=True)
    return oauth.google.authorize_redirect(redirect_uri, access_type="offline")


@app.route("/auth/google")
def auth_google():
    token = oauth.google.authorize_access_token()

    # upsert user to database
    User.replace(
        name=token["userinfo"]["name"],
        email=token["userinfo"]["email"],
        access_token=token["access_token"],
        refresh_token=token["refresh_token"],
    ).execute()

    # save user email to session
    session["user_email"] = token["userinfo"]["email"]

    return redirect("/")


@app.route("/logout")
def logout():
    session.pop("user_email", None)
    return redirect("/")
