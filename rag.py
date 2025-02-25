import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Protocol
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    Document,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
import streamlit as st
from config import AZURE_CONFIG

@dataclass
class AzureConfig:
    """Azure OpenAI configuration settings."""
    endpoint: str
    api_key: str
    embedding_deployment: str
    embedding_api_version: str
    chat_deployment: str
    chat_api_version: str
    model: str
    temperature: float

class DocumentLoader(Protocol):
    """Protocol for document loading strategies."""
    def load_documents(self, directory: str) -> List[Document]:
        """Load documents from a directory."""
        pass

class DefaultDocumentLoader:
    """Default implementation of document loading."""
    def load_documents(self, directory: str) -> List[Document]:
        documents = SimpleDirectoryReader(
            directory,
            required_exts=[".txt", ".pdf", ".md", ".docx"],
            recursive=True
        ).load_data()
        
        return [Document(text=str(doc.text).strip()) 
                for doc in documents 
                if str(doc.text).strip()]

class IndexManager:
    """Manages vector store index operations."""
    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir

    def load_existing_index(self) -> Optional[VectorStoreIndex]:
        """Try to load an existing index from storage."""
        try:
            if os.path.exists(self.storage_dir):
                storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
                return load_index_from_storage(storage_context)
        except Exception as e:
            st.error(f"Error loading existing index: {e}")
        return None

    def create_index(self, documents: List[Document]) -> VectorStoreIndex:
        """Create a new index from documents."""
        if not documents:
            raise ValueError("No valid documents to process")
        
        index = VectorStoreIndex.from_documents(
            documents,
            show_progress=False,
            embed_model=Settings.embed_model
        )
        
        self._persist_index(index)
        return index

    def _persist_index(self, index: VectorStoreIndex) -> None:
        """Persist the index to storage."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        index.storage_context.persist(persist_dir=self.storage_dir)

class RAGSystem:
    """Main RAG system implementation."""
    def __init__(
        self,
        config: AzureConfig,
        document_loader: DocumentLoader = DefaultDocumentLoader(),
        storage_dir: str = "storage"
    ):
        self._initialize_models(config)
        self.document_loader = document_loader
        self.index_manager = IndexManager(storage_dir)
        self.index = self.index_manager.load_existing_index()

    def _initialize_models(self, config: AzureConfig) -> None:
        """Initialize embedding and LLM models."""
        embed_model = AzureOpenAIEmbedding(
            azure_deployment_name=config.embedding_deployment,
            api_key=config.api_key,
            azure_endpoint=config.endpoint,
            api_version=config.embedding_api_version,
            max_retries=3
        )
        
        llm = AzureOpenAI(
            model=config.model,
            deployment_name=config.chat_deployment,
            azure_endpoint=config.endpoint,
            api_key=config.api_key,
            api_version=config.chat_api_version,
            temperature=config.temperature
        )
        
        Settings.embed_model = embed_model
        Settings.llm = llm

    def load_documents(self, directory: str = "documents") -> VectorStoreIndex:
        """Load documents and create or update the index."""
        try:
            with st.spinner("Loading documents..."):
                documents = self.document_loader.load_documents(directory)
                
                if not documents:
                    raise ValueError(f"No supported documents found in {directory}")
                
                with st.spinner("Creating document index..."):
                    self.index = self.index_manager.create_index(documents)
                return self.index
                
        except Exception as e:
            st.error(f"Error loading documents: {str(e)}")
            raise

    def query_documents(self, query: str) -> str:
        """Query the document index with a question."""
        if self.index is None:
            raise ValueError("No index available. Please initialize the system first.")
            
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query)
        return str(response)

def get_rag_system() -> RAGSystem:
    """Get or create a RAG system instance."""
    if "rag_system" not in st.session_state:
        config = AzureConfig(
            endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
            api_key=st.secrets["AZURE_OPENAI_KEY"],
            embedding_deployment=st.secrets["EMBEDDING_DEPLOYMENT"],
            embedding_api_version=st.secrets["EMBEDDING_API_VERSION"],
            chat_deployment=st.secrets["CHAT_DEPLOYMENT"],
            chat_api_version=st.secrets["CHAT_API_VERSION"],
            model=AZURE_CONFIG["model"],
            temperature=AZURE_CONFIG["temperature"]
        )
        st.session_state.rag_system = RAGSystem(config)
    return st.session_state.rag_system

if __name__ == "__main__":
    rag = RAGSystem()
    
    if rag.index is None:
        st.info("Creating new index...")
        rag.load_documents("documents")
    else:
        st.info("Using existing index...")
    
    test_query = "What information can you tell me about the documents?"
    try:
        response = rag.query_documents(test_query)
        st.write("Test Query:", test_query)
        st.write("Response:", response)
    except Exception as e:
        st.error(f"Error during query: {e}") 