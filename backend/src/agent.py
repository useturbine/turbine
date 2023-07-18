from langchain.llms import OpenAI
from langchain.docstore.document import Document
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import pathlib
import subprocess
import tempfile


class DocsData:
    @staticmethod
    def get_terraform_files():
        return []

    @staticmethod
    def get_cost_files():
        return []

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
        splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
        for source in sources:
            for chunk in splitter.split_text(source.page_content):
                chunks.append(Document(page_content=chunk, metadata=source.metadata))

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
        Use the context below to advise how to improve AWS based services by cost reduction and resource optimization:
        Context: {context}
        Topic: {topic}
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "topic"])

        llm = OpenAI(temperature=0)
        self.chain = LLMChain(llm=llm, prompt=prompt)

    def ask(self, topic):
        return self.chain.run({
            'context': self.context,
            topic: topic
        })


resp = PromptSystem().ask("aws cost reduction")
print(resp)
