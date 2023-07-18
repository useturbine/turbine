import subprocess
import boto3
from datetime import datetime, timedelta

from models import User


def terraform_aws(user_email: str):
    user = User.get(User.email == user_email)
    output_file = f"{user.email}.tfstate"

    subprocess.run(
        f"""
            terracognita aws --aws-access-key {user.aws_access_key} \
                --aws-secret-access-key {user.aws_secret_key} \
                --aws-default-region ap-south-1 \
                --tfstate {output_file}""",
        shell=True,
    )

    with open(output_file, "r") as f:
        user.aws_terraform = f.read()
        user.save()
    subprocess.run(f"rm {output_file}", shell=True)


def get_aws_cost(user_email: str):
    user = User.get(User.email == user_email)
    cost_explorer = boto3.client(
        "ce",
        region_name="ap-south-1",
        aws_access_key_id=user.aws_access_key,
        aws_secret_access_key=user.aws_secret_key,
    )

    current_date = datetime.now()
    one_month_ago = current_date - timedelta(days=30)

    response = cost_explorer.get_cost_and_usage(
        TimePeriod={
            "Start": one_month_ago.strftime("%Y-%m-%d"),
            "End": current_date.strftime("%Y-%m-%d"),
        },
        Granularity="DAILY",
        Metrics=["BlendedCost"],
        GroupBy=[
            {"Type": "DIMENSION", "Key": "SERVICE"},
            {"Type": "DIMENSION", "Key": "OPERATION"},
        ],
    )
    return response["ResultsByTime"]
