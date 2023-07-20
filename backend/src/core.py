import subprocess
import boto3
import tempfile
from datetime import datetime

from models import User, AWSCost
from peewee import IntegrityError


class AWS:
    """
    AWS class to interact with AWS.
    """

    def __init__(self, user_email: str, region: str):
        self.region = region
        self.user = User.get(User.email == user_email)
        self.cost_explorer = boto3.client(
            "ce",
            region_name=region,
            aws_access_key_id=self.user.aws_access_key,
            aws_secret_access_key=self.user.aws_secret_key,
        )

    def update_terraform(self):
        """
        Fetch Terraform files from AWS and store them in the database.
        """
        # create temporary file for storing Terraform file
        with tempfile.NamedTemporaryFile() as output_file:
            subprocess.run(
                f"""terracognita aws --aws-access-key {self.user.aws_access_key} \
                        --aws-secret-access-key {self.user.aws_secret_key} \
                        --aws-default-region {self.region} \
                        --hcl {output_file.name}""",
                shell=True,
            )
            # read Terraform file and store it in the database
            output_file.seek(0)
            self.user.aws_terraform = output_file.read()
            self.user.save()

    def update_costs(self, start_time: datetime, end_time: datetime):
        """
        Fetch AWS costs of the user and store them in the database.
        """
        # fetch costs from AWS
        response = self.cost_explorer.get_cost_and_usage(
            TimePeriod={
                "Start": start_time.strftime("%Y-%m-%d"),
                "End": end_time.strftime("%Y-%m-%d"),
            },
            Granularity="DAILY",
            Metrics=["BlendedCost"],
            GroupBy=[
                {"Type": "DIMENSION", "Key": "SERVICE"},
                {"Type": "DIMENSION", "Key": "OPERATION"},
            ],
        )
        results = response["ResultsByTime"]

        # format results into list of dicts for insertion to database
        aws_costs = []
        for result in results:
            for group in result["Groups"]:
                aws_costs.append(
                    {
                        "user": self.user.id,
                        "start_time": result["TimePeriod"]["Start"],
                        "end_time": result["TimePeriod"]["End"],
                        "service": group["Keys"][0],
                        "operation": group["Keys"][1],
                        "cost": group["Metrics"]["BlendedCost"]["Amount"],
                        "region": self.region,
                    }
                )

        # try bulk insert
        try:
            AWSCost.insert_many(aws_costs).execute()
        # if it fails, switch to slower individual insert
        except IntegrityError:
            for aws_cost in aws_costs:
                try:
                    AWSCost.insert(**aws_cost).execute()
                except IntegrityError:
                    pass
