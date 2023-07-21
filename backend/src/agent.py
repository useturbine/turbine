from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain.schema.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    messages_from_dict,
)
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from models import User, Message
from config import openai_api_key
from typing import List
from langchain.schema import (
    BaseChatMessageHistory,
)
from langchain.schema.messages import BaseMessage


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
        print(
            [
                {
                    "type": "human" if message.is_human else "ai",
                    "data": message.content,
                }
                for message in messages
            ]
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


class Chain:
    def __init__(self, user_email: str) -> None:
        user = User.get(User.email == user_email)
        memory = ConversationBufferMemory(
            chat_memory=DatabaseChatMessageHistory(user_email=user_email),
            return_messages=True,
        )
        llm = ChatOpenAI(
            temperature=0, openai_api_key=openai_api_key, model="gpt-3.5-turbo-16k"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=f"""
                    You are a cloud architect. You have been provided the following Terraform file which is deployed on AWS.
                    You don't tell the user that you got the information from a Terraform file. You just answer the question.
                    You do not give very detailed answers. You just answer the question and keep it as simple as you can so that the user can understand.
                    
                    {user.aws_terraform}
                    """
                ),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

        self.conversation = ConversationChain(
            memory=memory,
            prompt=prompt,
            llm=llm,
            verbose=True,
        )

    def talk(self, input: str):
        return self.conversation.predict(input=input)


chain = Chain(user_email="sumit.ghosh32@gmail.com")
chain.conversation.memory.chat_memory.clear()

response = chain.talk(input="Hi! I'm Sumit.")
print(response)
response = chain.talk(input="Do I have any EC2 instances?")
print(response)
