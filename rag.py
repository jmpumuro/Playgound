import os
from typing import List, Optional
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, Document, StorageContext, load_index_from_storage
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
import streamlit as st
from config import AZURE_CONFIG

class RAGSystem:
    def __init__(self):
        # Initialize Azure OpenAI settings
        self.azure_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
        self.api_key = st.secrets["AZURE_OPENAI_KEY"]
        self.embedding_deployment = st.secrets["EMBEDDING_DEPLOYMENT"]
        self.storage_dir = "tmp/storage"  # Directory to store the index
        
        # Initialize embedding model with deployment name
        embed_model = AzureOpenAIEmbedding(
            azure_deployment_name=self.embedding_deployment,
            api_key=self.api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=st.secrets["EMBEDDING_API_VERSION"],
            max_retries=3
        )
        
        # Set the embedding model as default
        Settings.embed_model = embed_model
        
        # Initialize LLM
        llm = AzureOpenAI(
            model=AZURE_CONFIG["model"],
            deployment_name=st.secrets["CHAT_DEPLOYMENT"],
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version=st.secrets["CHAT_API_VERSION"],
            temperature=AZURE_CONFIG["temperature"]
        )
        
        # Set the LLM
        Settings.llm = llm
        
        # Try to load existing index
        self.index = self.load_existing_index()
        
    def load_existing_index(self) -> Optional[VectorStoreIndex]:
        """Try to load an existing index from storage."""
        try:
            if os.path.exists(self.storage_dir):
                storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
                return load_index_from_storage(storage_context)
        except Exception as e:
            print(f"Error loading existing index: {e}")
        return None
        
    def load_documents(self, directory: str = "documents") -> VectorStoreIndex:
        """Load documents and create or update the index."""
        try:
            # Only load supported file types
            documents = SimpleDirectoryReader(
                directory,
                required_exts=[".txt", ".pdf", ".md", ".docx"],
                recursive=True
            ).load_data()
            
            if not documents:
                raise ValueError(f"No supported documents found in {directory}")
            
            print(f"Processing {len(documents)} documents")
            processed_docs = []
            for i, doc in enumerate(documents):
                print(f"Doc {i}: {doc.text[:50]}...")
                text = str(doc.text).strip()
                if text:
                    processed_docs.append(Document(text=text))
            
            if not processed_docs:
                raise ValueError("No valid documents to process")
            
            # Create new index
            self.index = VectorStoreIndex.from_documents(
                processed_docs,
                show_progress=True,
                embed_model=Settings.embed_model
            )
            
            # Save the index
            if not os.path.exists(self.storage_dir):
                os.makedirs(self.storage_dir)
            self.index.storage_context.persist(persist_dir=self.storage_dir)
            
            return self.index
            
        except Exception as e:
            print(f"Error loading documents: {str(e)}")
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
        st.session_state.rag_system = RAGSystem()
    return st.session_state.rag_system

if __name__ == "__main__":
    # Create RAG system
    rag = RAGSystem()
    
    # Check if index exists, if not create it
    if rag.index is None:
        print("Creating new index...")
        rag.load_documents("documents")
    else:
        print("Using existing index...")
    
    # Test query
    test_query = "What information can you tell me about the documents?"
    try:
        response = rag.query_documents(test_query)
        print("\nTest Query:", test_query)
        print("Response:", response)
    except Exception as e:
        print(f"Error during query: {e}") 