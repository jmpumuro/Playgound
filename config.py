import streamlit as st

# Page configuration
PAGE_CONFIG = {
    "page_title": "PLAYGROUND",
    "page_icon": "📝",
    "layout": "wide"
}

# Azure OpenAI configuration
AZURE_CONFIG = {
    "api_version": "2024-08-01-preview",
    "deployment_name": "dev-gpt-4o-mini",
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 800,
    "embedding_deployment": "text-embedding-3-large",
    "embedding_model": "text-embedding-3-large"
}