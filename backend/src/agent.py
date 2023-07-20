from langchain.llms import OpenAI
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import OPENAI_API_KEY

from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI


db = SQLDatabase.from_uri("sqlite:///./database.db")
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))


memory = ConversationBufferMemory(memory_key="chat_history")
llm = OpenAI(temperature=0)

agent = initialize_agent(
    llm=OpenAI(temperature=0),
    tools=toolkit.get_tools(),
    verbose=True,
    memory=memory,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)


answer = agent.run(
    input="My name is Sumit. Give me my total AWS cost in the past week."
)
print(answer)


class DocsData:
    @staticmethod
    def get_terraform_files():
        with open("./sample-terraform", "r") as f:
            d = f.read()
        return [d]

    @staticmethod
    def get_cost_files():
        with open("./sample-cost", "r") as f:
            d = f.read()
        return [d]

    @staticmethod
    def get_files():
        files = []

        files.extend(DocsData.get_terraform_files())
        files.extend(DocsData.get_cost_files())

        return files


class ChromaDocs(DocsData):
    def __init__(self):
        self.context = None

    def set(self):
        sources = DocsData.get_files()

        chunks = []
        splitter = CharacterTextSplitter(
            separator=" ", chunk_size=1024, chunk_overlap=0
        )
        for source in sources:
            for chunk in splitter.split_text(source):
                chunks.append(Document(page_content=chunk))

        self.context = Chroma.from_documents(chunks, OpenAIEmbeddings())

    def get(self):
        if self.context is not None:
            return self.context

        self.set()
        return self.context


class PromptSystem:
    def __init__(self):
        self.chroma_docs = ChromaDocs()
        self.context = self.chroma_docs.get()
        self.chain = None

        self.set()

    def set(self):
        prompt_template = """
        You are a cloud architect. You are asked to reduce the cost of a cloud infrastructure. Given the following context which contains the terraform plan and the cost of the last month, what would you advise?
        Context: {context}
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["context"])

        llm = OpenAI(temperature=0)
        self.chain = LLMChain(llm=llm, prompt=prompt)

    def ask(self, topic):
        return self.chain.run({"context": self.context, "topic": topic})
