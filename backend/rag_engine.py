"""
RAG (Retrieval-Augmented Generation) Engine using LangChain and FAISS.
Handles document ingestion and semantic search over embedded documents.
"""

from typing import List
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document


class RAGEngine:
    """
    RAG Engine for document retrieval using semantic search.
    Uses FAISS vector store and sentence-transformers for embeddings.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG Engine with embedding model.

        Args:
            model_name: HuggingFace model name for embeddings (default: all-MiniLM-L6-v2)
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.vector_store = None
        self.documents = []

    def ingest_documents(self, docs: List[str]) -> None:
        """
        Ingest documents by converting them to embeddings and storing in FAISS.

        Args:
            docs: List of document strings to embed and store

        Returns:
            None
        """
        if not docs:
            raise ValueError("Document list cannot be empty")

        # Store original documents for reference
        self.documents = docs

        # Convert strings to Document objects for LangChain
        document_objects = [
            Document(page_content=doc, metadata={"source": f"doc_{i}"})
            for i, doc in enumerate(docs)
        ]

        # Create FAISS vector store from documents
        # This will embed all documents using the HuggingFace embeddings model
        self.vector_store = FAISS.from_documents(document_objects, self.embeddings)

        print(f"Successfully ingested {len(docs)} documents into FAISS vector store")

    def query_documents(self, user_query: str, top_k: int = 3) -> str:
        """
        Query the document store using semantic similarity.
        Returns a formatted prompt string with retrieved documents.

        Args:
            user_query: The user's query string
            top_k: Number of top results to retrieve (default: 3)

        Returns:
            str: Formatted prompt string with retrieved documents and query
        """
        if self.vector_store is None:
            raise ValueError(
                "No documents have been ingested. Call ingest_documents() first."
            )

        if not user_query or not user_query.strip():
            raise ValueError("Query cannot be empty")

        # Retrieve top-k most similar documents using cosine similarity
        # FAISS uses similarity search by default
        retrieved_docs = self.vector_store.similarity_search(user_query, k=top_k)

        # Format retrieved documents into a single string
        formatted_docs = "\n---\n".join([doc.page_content for doc in retrieved_docs])

        # Create the strict prompt format
        prompt = f"""Answer the question using ONLY these documents.

Documents:
{formatted_docs}

Question: {user_query}"""

        return prompt

    def get_documents(self) -> List[str]:
        """
        Get the list of ingested documents.

        Returns:
            List of document strings
        """
        return self.documents

    def get_vector_store(self):
        """
        Get the underlying FAISS vector store.

        Returns:
            FAISS vector store object or None if documents haven't been ingested
        """
        return self.vector_store


# Example usage
if __name__ == "__main__":
    # Create RAG engine instance
    rag = RAGEngine()

    # Example documents
    sample_docs = [
        "Python is a high-level programming language known for its simplicity and readability.",
        "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
        "FastAPI is a modern web framework for building APIs with Python 3.6+.",
        "Vector databases like FAISS enable efficient similarity search at scale.",
        "Natural language processing (NLP) focuses on interactions between computers and human language.",
    ]

    # Ingest documents
    rag.ingest_documents(sample_docs)

    # Query the documents
    user_query = "What is Python used for?"
    prompt = rag.query_documents(user_query)

    print("Generated Prompt:")
    print("-" * 50)
    print(prompt)
    print("-" * 50)
