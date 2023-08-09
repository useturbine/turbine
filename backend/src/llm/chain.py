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
                    content="Your name is InfraBro, you are an expert in cloud infrastructure. "
                    "You will be provided with a Terraform file containing details about a cloud environment. "
                    "The answers should be simple and easy to understand for a non technical person. "
                    "Be precise, factual and professional in your replies. "
                    "Do not mention anything that is not asked. "
                    "Do not mention anything that is not related to the question. "
                    "Do not mention anything that is not related to the cloud infrastructure. "
                    "This is very important: Do not mention the Terraform file in your replies. "
                    "\nFollowing is the Terraform file. \n\n"
                    f"{user.aws_terraform}"
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
