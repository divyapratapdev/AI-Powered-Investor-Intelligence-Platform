import os
import uuid
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from ingestion.pdf_to_markdown import convert_pdf_to_markdown
from ingestion.semantic_chunker import chunk_text
from database.save_metrics import save_metrics
from rag.kpi_extractor_rag import extract_financial_metrics, Retriever
from vectorstore.azure_ai_search import AzureAISearchVectorStore


def ingest_pdf(
    pdf_bytes: bytes,
    filename: str,
    endpoint: str,
    api_key: str,
    index_name: str
) -> dict:
    # Extract company and year from filename (e.g. 2024_Apple.pdf)
    parts = os.path.splitext(filename)[0].split("_")
    year = parts[0] if parts else "unknown"
    company = "_".join(parts[1:]) if len(parts) > 1 else "unknown"

    # Convert PDF to markdown
    markdown = convert_pdf_to_markdown(pdf_bytes)

    # Chunk the text
    chunks = chunk_text(markdown)

    # Upload chunks to Azure AI Search
    search_client = SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(api_key)
    )

    docs = [
        {"id": str(uuid.uuid4()), "content": chunk, "company": company, "year": year}
        for chunk in chunks
    ]

    search_client.upload_documents(documents=docs)

    # Extract KPIs using RAG
    store = AzureAISearchVectorStore(endpoint=endpoint, api_key=api_key, index_name=index_name)
    retriever = Retriever(store.client)
    metrics = extract_financial_metrics(retriever=retriever, company=company, year=int(year))

    # Save metrics to database
    save_metrics(company=company, year=int(year), metrics=metrics)

    return {"company": company, "year": year, "chunks_uploaded": len(chunks)}
