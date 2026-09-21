import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential


class AzureAISearchVectorStore:
    def __init__(self, endpoint: str, api_key: str, index_name: str):
        self.client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key)
        )
