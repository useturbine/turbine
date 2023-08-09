from langchain.tools import tool
import boto3
from src.config import aws_access_key, aws_secret_key


def describe_instances() -> str:
    """Get list of available EC2 instances in the AWS account."""
    ec2_client = boto3.client(
        "ec2",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name="ap-south-1",
    )
    response = ec2_client.describe_instances()
    print(response)
