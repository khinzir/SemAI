"""
Azure AI Search client for RAG operations
"""
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, SearchField,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile
)


class SearchClientManager:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.key = os.getenv("AZURE_SEARCH_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX", "csit-sem1-index")

        self.search_client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=AzureKeyCredential(self.key)
        )

    def search(self, query: str, semester: int = 1, subject: str = None, top: int = 5):
        """Search for relevant documents"""
        filter_string = f"semester eq {semester}"
        if subject:
            filter_string += f" and subject eq '{subject}'"

        results = self.search_client.search(
            search_text=query,
            filter=filter_string,
            top=top,
            include_total_count=True
        )

        return [{
            "content": doc["content"],
            "source": doc.get("source_file", "Unknown"),
            "subject": doc.get("subject", ""),
            "relevance_score": doc.get("@search.score", 0)
        } for doc in results]

    def create_index(self):
        """Create the search index (run once)"""
        index_client = SearchIndexClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )

        fields = [
            SimpleField(name="id", type="Edm.String", key=True),
            SearchableField(name="content", type="Edm.String", analyzer_name="en.microsoft"),
            SimpleField(name="semester", type="Edm.Int32", filterable=True, facetable=True),
            SimpleField(name="subject", type="Edm.String", filterable=True, facetable=True),
            SimpleField(name="unit", type="Edm.String", filterable=True),
            SimpleField(name="document_type", type="Edm.String", filterable=True),
            SimpleField(name="source_file", type="Edm.String"),
            SimpleField(name="year", type="Edm.Int32", filterable=True),
            SimpleField(name="has_solution", type="Edm.Boolean"),
            # FIXED FOR PYTHON: Using SearchField with vector dimensions parameter keys
            SearchField(
                name="content_vector",
                type="Collection(Edm.Single)",
                vector_search_dimensions=1536,
                vector_search_profile_name="vector-profile"
            )
        ]


        vector_search = VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(name="hnsw-config")
            ],
            profiles=[
                # CHANGE algorithm_name TO algorithm_configuration_name HERE:
                VectorSearchProfile(name="vector-profile", algorithm_configuration_name="hnsw-config")
            ]
        )

        index = SearchIndex(name=self.index_name, fields=fields, vector_search=vector_search)
        result = index_client.create_or_update_index(index)
        return result

    def upload_document(self, document: dict):
        """Upload a single document to the index"""
        try:
            result = self.search_client.upload_documents(documents=[document])
            return result
        except Exception as e:
            print(f"Error uploading document: {e}")
            return None