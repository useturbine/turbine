import httpx
from turbine.database import User, Session
from sqlalchemy import select
from .config import config


def main():
    response = httpx.get(
        "https://api.clerk.com/v1/users?offset=0&order_by=created_at&limit=100",
        headers={"Authorization": f"Bearer {config.clerk_secret_key}"},
    )
    clerk_users = response.json()

    with Session() as db:
        for clerk_user in clerk_users:
            stmt = select(User).where(
                User.clerk_id == clerk_user["id"], User.deleted == False
            )
            user = db.scalars(stmt).one_or_none()
            if not user:
                print(
                    f"Adding user {clerk_user['first_name']} {clerk_user['last_name']}"
                )
                db.add(User(clerk_id=clerk_user["id"]))
        db.commit()


if __name__ == "__main__":
    main()
