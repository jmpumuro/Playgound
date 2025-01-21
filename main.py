import streamlit as st
from config import PAGE_CONFIG
from styles import CUSTOM_CSS
from azure_client import init_azure_openai, generate_summary
from ui_components import (
    render_prompt_section,
    render_transcript_section,
    render_results,
)

def main():
    # Configure page
    st.set_page_config(**PAGE_CONFIG)
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    st.title("Session Summary")
    
    # Initialize Azure OpenAI client
    client = init_azure_openai()
    if not client:
        st.error("Please configure Azure OpenAI credentials in streamlit secrets.")
        return
    
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
    

if __name__ == "__main__":
    main()