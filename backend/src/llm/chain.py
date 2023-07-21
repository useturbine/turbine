from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain.schema.messages import SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from src.models import User
from src.config import openai_api_key
from src.llm.memory import DatabaseChatMessageHistory


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
