import os
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType
from azure.core.credentials import AzureKeyCredential


def create_index(endpoint: str, api_key: str, index_name: str) -> None:
    client = SearchIndexClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="content", type=SearchFieldDataType.String, searchable=True),
        SimpleField(name="company", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="year", type=SearchFieldDataType.String, filterable=True),
    ]

    index = SearchIndex(name=index_name, fields=fields)

    try:
        client.create_or_update_index(index)
        print(f"Index '{index_name}' created or updated.")
    except Exception as e:
        print(f"Index creation warning: {e}")
