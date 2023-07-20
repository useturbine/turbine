from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.models import User
from src.config import webapp_url

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[webapp_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegisterArgs(BaseModel):
    email: str
    name: str | None = None


@app.post("/register")
async def register(args: RegisterArgs):
    user = User.create(email=args.email, name=args.name)
    return {"id": user.id}


class AWSUpdateCredentialsArgs(BaseModel):
    user_email: str
    access_key: str
    secret_key: str


@app.post("/aws/update-credentials")
async def aws_update_credentials(args: AWSUpdateCredentialsArgs):
    user = User.get(User.email == args.user_email)
    user.aws_access_key = args.access_key
    user.aws_secret_key = args.secret_key
    user.save()
    return
