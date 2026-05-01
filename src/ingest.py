from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

load_dotenv()

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL")
PGVECTOR_CONNECTION = os.getenv("PGVECTOR_CONNECTION")

class Ingest:
    def run(self):
        print("Iniciando a ingestão do documento...")
        base_dir_path = Path(__file__).parent
        docs = PyPDFLoader(base_dir_path / "document.pdf").load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, add_start_index=True
        )
        splits = text_splitter.split_documents(docs)

        embedding = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
        db_connection = PGVector.from_documents(
            embedding=embedding,
            documents=splits,
            connection=PGVECTOR_CONNECTION,
        )
        print("Ingestão concluída, pronto para responder suas perguntas!\nUse o comando 'python src/chat.py' para iniciar o chat.")

if __name__ == "__main__":
    Ingest().run()