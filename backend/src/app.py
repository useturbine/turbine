from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth

from utils import read_yaml_file

cfg = read_yaml_file("config.yaml")

app = Flask(__name__)
app.secret_key = cfg.App.SecretKey

oauth = OAuth(app)


@app.route("/google/")
def google():
    oauth.register(
        name="google",
        client_id=cfg.Google.CLIENT_ID,
        client_secret=cfg.Google.CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    redirect_uri = url_for("app.google_auth", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/google/auth/")
def google_auth():
    token = oauth.google.authorize_access_token()
    user_dict = oauth.google.parse_id_token(token, None)

    # save in DB here if needed
    # info in user_dict

    return redirect("/")
