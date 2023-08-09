import os
from dotenv import load_dotenv

from src.llm.chain import Chain
from src.models import User
from src.cloud.aws import AWS

load_dotenv()

# If database is empty, create a user
if User.select().count() == 0:
    user = User.create(
        email="sumit.ghosh32@gmail.com",
        name="Sumit Ghosh",
        aws_access_key=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_key=os.getenv("AWS_SECRET_KEY"),
    )
else:
    user = User.get(User.email == "sumit.ghosh32@gmail.com")

# If Terraform file is not present, get it from AWS
if user.aws_terraform is None:
    aws = AWS(user_email="sumit.ghosh32@gmail.com", region="ap-south-1")
    aws.update_terraform()


# Initialize the chain and clear the memory
chain = Chain(user_email="sumit.ghosh32@gmail.com")
chain.conversation.memory.chat_memory.clear()

# Start the conversation
response = chain.talk(input="Hi! I'm Sumit.")
print(response)
response = chain.talk(input="Do I have any EC2 instances?")
print(response)

# Start the conversation
# response = chain.talk(input="Hi! I'm Sumit.")
# print(response)
# response = chain.talk(input="Do I have any EC2 instances?")
# print(response)


# from langchain.agents import create_sql_agent
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from langchain.sql_database import SQLDatabase
# from langchain.llms.openai import OpenAI
# from langchain.agents import AgentExecutor
# from langchain.agents.agent_types import AgentType
# from langchain.chat_models import ChatOpenAI

# from src.config import openai_api_key

# db = SQLDatabase.from_uri("sqlite:///database.db")
# toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))


# agent_executor = create_sql_agent(
#     llm=OpenAI(temperature=0, openai_api_key=openai_api_key),
#     toolkit=toolkit,
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# )

# answer = agent_executor.run(
#     "I'm Sumit Ghosh, what are my total ec2 costs for this month?"
# )
# print(answer)
