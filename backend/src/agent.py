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

from models import User
from config import openai_api_key


class Chain:
    def __init__(self, user_email: str) -> None:
        user = User.get(User.email == user_email)
        memory = ConversationBufferMemory(return_messages=True)
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
response = chain.talk(input="Hi! I'm Sumit.")
print(response)
response = chain.talk(input="Do I have any EC2 instances?")
print(response)
