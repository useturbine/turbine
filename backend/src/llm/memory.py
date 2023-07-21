from langchain.schema.messages import (
    HumanMessage,
    AIMessage,
    messages_from_dict,
)
from typing import List
from langchain.schema import (
    BaseChatMessageHistory,
)
from langchain.schema.messages import BaseMessage

from src.models import User, Message


class DatabaseChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, user_email: str) -> None:
        self.user = User.get(User.email == user_email)

    def add_message(self, message: BaseMessage) -> None:
        if isinstance(message, HumanMessage):
            Message.create(
                content=message.content,
                user=self.user,
                is_human=True,
            )

        elif isinstance(message, AIMessage):
            Message.create(
                content=message.content,
                user=self.user,
                is_human=False,
            )

    def clear(self) -> None:
        Message.update(latest=False).where(Message.user == self.user).execute()

    @property
    def messages(self) -> List[BaseMessage]:
        messages = Message.select().where(
            Message.user == self.user, Message.latest == True
        )
        messages = messages_from_dict(
            [
                {
                    "type": "human" if message.is_human else "ai",
                    "data": {"content": message.content},
                }
                for message in messages
            ]
        )
        return messages
