import streamlit as st
from openai import AzureOpenAI
from config import AZURE_CONFIG

def init_azure_openai():
    """Initialize Azure OpenAI client"""
    try:
        # Construct the full endpoint URL
        base_url = st.secrets["AZURE_OPENAI_ENDPOINT"]
        deployment = st.secrets["CHAT_DEPLOYMENT"]
        api_version = AZURE_CONFIG["api_version"]
        
        # Remove any trailing slashes and construct the endpoint
        base_url = base_url.rstrip('/')
        azure_endpoint = f"{base_url}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
        
        client = AzureOpenAI(
            api_key=st.secrets["AZURE_OPENAI_KEY"],
            api_version=AZURE_CONFIG["api_version"],
            azure_endpoint=azure_endpoint
        )
        
        # Test the client with a simple request
        try:
            response = client.chat.completions.create(
                model=AZURE_CONFIG["model"],
                messages=[{"role": "system", "content": "Test"}],
                max_tokens=5
            )
        except Exception as e:
            print(f"Test request failed: {str(e)}")
            raise e
            
        return client
    except Exception as e:
        st.error(f"Error initializing Azure OpenAI: {str(e)}")
        return None

def generate_summary(client, prompt, transcript):
    """Generate summary using Azure OpenAI"""
    try:
        # Add validation and logging
        if not prompt or not transcript:
            st.error("Prompt or transcript is empty")
            return None
            
        # Log the request parameters (for debugging)
        ''' st.write("Debug info:")
        st.write(f"Model: {AZURE_CONFIG['model']}")
        st.write(f"Prompt length: {len(prompt)}")
        st.write(f"Transcript length: {len(transcript)}") '''
        
        response = client.chat.completions.create(
            model=AZURE_CONFIG["model"],
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": transcript}
            ],
            temperature=AZURE_CONFIG["temperature"],
            max_tokens=AZURE_CONFIG["max_tokens"],
            # Add these parameters for better error handling
            timeout=60,
            presence_penalty=0,
            frequency_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        # More detailed error logging
        st.error(f"Error generating summary: {str(e)}")
        if hasattr(e, 'response'):
            st.error(f"Response status: {e.response.status_code}")
            st.error(f"Response body: {e.response.text}")
        return None