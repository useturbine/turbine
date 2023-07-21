from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.models import User
from src.config import webapp_url
from src.llm.chain import Chain

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


class ChatArgs(BaseModel):
    user_email: str
    message: str


@app.post("/chat")
async def chat(args: ChatArgs):
    chain = Chain(args.user_email)
    return {"response": chain.talk(args.message)}
