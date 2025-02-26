import streamlit as st
import os
import nltk
from pathlib import Path

nltk_data_dir = '/tmp/nltk_data' 
os.environ['NLTK_DATA'] = nltk_data_dir

if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir, exist_ok=True)

required_packages = ['stopwords', 'punkt', 'averaged_perceptron_tagger', 'wordnet']
for package in required_packages:
    try:
        nltk.download(package, download_dir=nltk_data_dir, quiet=True)
    except Exception as e:
        st.warning(f"Failed to download NLTK package {package}: {str(e)}")

nltk.data.path.insert(0, nltk_data_dir)

# Now import the rest of the dependencies
from config import PAGE_CONFIG
from styles import CUSTOM_CSS
from azure_client import init_azure_openai, generate_summary
from components.ui_components import (
    render_prompt_section,
    render_transcript_section,
    render_results,
)
from components.reflection import render_reflection_section
from components.stress_reduction import StressReductionChat

def main():
    # Configure page
    st.set_page_config(**PAGE_CONFIG)
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    st.title("PLAYGROUND")
    
    # Initialize Azure OpenAI client
    client = init_azure_openai()
    if not client:
        st.error("Please configure Azure OpenAI credentials in streamlit secrets.")
        return
    
    # Create main tabs
    summary_tab, reflection_tab, stress_tab = st.tabs(["Session Summary", "Daily Reflection", "Stress Reduction"])
    
    with summary_tab:
        # Main content
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                prompt, api_config = render_prompt_section()
            
            with col2:
                transcript = render_transcript_section()
        
        # Generate Summary button
        if st.button("Generate Summary", type="primary"):
            if not transcript:
                st.warning("Please enter or select a transcript to analyze.")
                return
            
            if not prompt and not api_config:
                st.warning("Please select or enter a prompt template.")
                return
                
            with st.spinner("Generating summary..."):
                if api_config:
                    st.error("Custom API implementation not yet available")
                    return
                else:
                    summary = generate_summary(client, prompt, transcript)
                
                if summary:
                    render_results(transcript, summary, api_config)
    
    with reflection_tab:
        render_reflection_section(client)
        
    with stress_tab:
        chat = StressReductionChat()
        chat.render_interface()

if __name__ == "__main__":
    main()