import os
from dotenv import load_dotenv

from src.llm.chain import Chain
from src.models import User
from src.cloud.aws import AWS

load_dotenv()

# If database is empty, create a user
if User.select().count() == 0:
    User.create(
        email="sumit.ghosh32@gmail.com",
        name="Sumit Ghosh",
        aws_access_key=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_key=os.getenv("AWS_SECRET_KEY"),
    )
    aws = AWS(user_email="sumit.ghosh32@gmail.com")
    aws.update_terraform()


# Initialize the chain and clear the memory
chain = Chain(user_email="sumit.ghosh32@gmail.com")
chain.conversation.memory.chat_memory.clear()

# Start the conversation
response = chain.talk(input="Hi! I'm Sumit.")
print(response)
response = chain.talk(input="Do I have any EC2 instances?")
print(response)
