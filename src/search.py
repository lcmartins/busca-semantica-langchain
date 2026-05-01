from dotenv import load_dotenv
from langchain_classic.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
import os

load_dotenv()
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL")
PGVECTOR_CONNECTION = os.getenv("PGVECTOR_CONNECTION")
LLM_MODEL = os.getenv("LLM_MODEL")

class Search:
    _instance = None
    store = None
    
    @staticmethod
    def instance():
        if Search._instance is None:
            search_instance = Search()
            search_instance.store = PGVector(
                connection=PGVECTOR_CONNECTION,
                embeddings=OpenAIEmbeddings(model=EMBEDDINGS_MODEL),
            )
    
            search_instance.llm_chat = ChatOpenAI(
                model=LLM_MODEL,
                temperature=0,
                max_tokens=10000
            )

            search_instance.retriever = search_instance.store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 10}
            )
            prompt_template = """CONTEXTO (10 resultados mais relevantes):
    {context}

    REGRAS GERAIS:
    - Responda SOMENTE com base no CONTEXTO fornecido acima.
    - Para CADA um dos 10 resultados incluidos no CONTEXTO, gere uma resposta separada à pergunta do usuário.
    - Cada resposta deve usar APENAS as informações presentes no respectivo resultado; não use conhecimento externo.
    - Se um resultado não contiver informação suficiente, responda para esse item: "Não tenho informações necessárias para responder sua pergunta."
    - Não produza opiniões ou inferências além do que está escrito.

    FORMATO DE SAÍDA (obrigatório):
    Retorne exatamente 10 respostas numeradas (uma para cada resultado do contexto):

    1. [resposta baseada no resultado 1]
    2. [resposta baseada no resultado 2]
    3. [resposta baseada no resultado 3]
    ... (até 10)

    Se um resultado não tiver informação suficiente, escreva: "Não tenho informações necessárias para responder sua pergunta."

    PERGUNTA DO USUÁRIO:
    {input}

    RESPOSTAS (10 itens numerados):"""

            search_instance.prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["input", "context"]
            )
            document_chain = create_stuff_documents_chain(
                llm=search_instance.llm_chat,
                prompt=search_instance.prompt
            )
            Search._instance = search_instance
        return Search._instance

    def search(self, query):
        docs = self.retriever.invoke(query)
        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )
        prompt = self.prompt.format(
            input=query,
            context=context
        )
        response = self.llm_chat.invoke(prompt)
        return response.content