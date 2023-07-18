import subprocess
from src.models import User


def terraform_aws(user_email: str):
    user = User.get(User.email == user_email)
    output_file = f"{user.email}.tfstate"

    subprocess.run(
        f"""
            terracognita aws --aws-access-key {user.aws_access_key}
                --aws-secret-access-key {user.aws_secret_key}
                --aws-default-region ap-south-1
                --tfstate {output_file}""",
        shell=True,
    )

    with open(output_file, "r") as f:
        user.aws_terraform = f.read()
        user.save()
    subprocess.run(f"rm {output_file}", shell=True)


terraform_aws("sumit.ghosh32@gmail.com")
