from langchain.tools import tool
import boto3
import os
from dotenv import load_dotenv
from pprint import pprint
from langchain import (
    LLMMathChain,
    OpenAI,
    SerpAPIWrapper,
    SQLDatabase,
    SQLDatabaseChain,
)
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI


load_dotenv()


def describe_instances() -> str:
    """
    Get list of available EC2 instances in the AWS account.
    """
    ec2_client = boto3.client(
        "ec2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name="ap-south-1",
    )
    response = ec2_client.describe_instances()
    print(response)


# @tool
def list_buckets() -> str:
    """
    Get the names of available S3 buckets in the AWS account.

    Output is a string of bucket names separated by newline.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    )
    buckets = s3_client.list_buckets()["Buckets"]
    bucket_names = [bucket["Name"] for bucket in buckets]
    return "\n".join(bucket_names)


# @tool
def create_bucket(name: str) -> str:
    """
    Create a new S3 bucket in the AWS account.
    Before invoking this tool, make sure that the bucket name is available.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    )
    s3_client.create_bucket(
        Bucket=name, CreateBucketConfiguration={"LocationConstraint": "ap-south-1"}
    )
    return f"Created bucket {name}."


llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
# tools = [list_buckets, create_bucket]
tools = [
    Tool(
        name="List Buckets",
        func=list_buckets,
        description="Can be used to check if a bucket already exists or not. Get the names of available S3 buckets in the AWS account. Output is a string of bucket names separated by newline.",
    ),
    Tool(
        name="Create Bucket",
        func=create_bucket,
        description="Create a new S3 bucket in the AWS account.",
    ),
]
memory = ConversationBufferMemory(memory_key="chat_history")


agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
)
output = agent.run("If a bucket named lordgabentruly does not exist, create it.")
print(output)
