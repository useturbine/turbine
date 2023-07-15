import os
from dotenv import load_dotenv
from dotmap import DotMap

load_dotenv()
config = DotMap()

config.app.secret_key = os.getenv("SECRET_KEY")
config.google.client_id = os.getenv("GOOGLE_CLIENT_ID")
config.google.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
