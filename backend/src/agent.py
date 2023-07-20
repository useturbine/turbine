from langchain.llms import OpenAI
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


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


resp = PromptSystem().ask()
print(resp)
