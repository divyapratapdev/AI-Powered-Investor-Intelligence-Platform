import os
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


def chunk_text(text: str) -> list[str]:
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_EMBEDDING_VERSION"),
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    )

    chunker = SemanticChunker(embeddings)
    docs = chunker.create_documents([text])
    return [doc.page_content for doc in docs]
