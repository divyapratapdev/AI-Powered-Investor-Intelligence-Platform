import os
import sys
from dotenv import load_dotenv

load_dotenv()

from vectorstore.azure_ai_search import AzureAISearchVectorStore


def search_vectorstore(query: str, top: int = 5):
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    api_key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

    store = AzureAISearchVectorStore(endpoint=endpoint, api_key=api_key, index_name=index_name)
    results = list(store.client.search(query, top=top))

    print(f"Query: {query!r}")
    print(f"Results: {len(results)}\n")

    for idx, result in enumerate(results, start=1):
        content = result.get("content", "<no content>")
        snippet = content.strip().replace("\n", " ")[:350]
        print(f"Result {idx}: {snippet}")
        print("  " + "-" * 60)

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m rag.retrieval_debug \"your query\"")
        sys.exit(1)
    search_vectorstore(" ".join(sys.argv[1:]))
