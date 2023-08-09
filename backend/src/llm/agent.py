from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

from src.config import openai_api_key

db = SQLDatabase.from_uri("sqlite:///database.db")
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))


agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0, openai_api_key=openai_api_key, model="gpt-3.5-turbo-16k"),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

answer = agent_executor.run("Describe the awscosts table")
print(answer)
