import streamlit as st
from azure_client import init_azure_openai
from config import AZURE_CONFIG
from rag import get_rag_system
from stress_reduction_prompts import DEFAULT_SYSTEM_PROMPT
from modal import open_modal_dialog
import time
import re

def get_azure_client():
    """Get or initialize Azure OpenAI client"""
    if 'azure_client' not in st.session_state:
        client = init_azure_openai()
        if client is None:
            st.error("Failed to initialize Azure OpenAI client. Please check your credentials.")
            st.stop()
        st.session_state.azure_client = client
    return st.session_state.azure_client

def get_relevant_resources(query: str) -> str:
    """Get relevant resources from the RAG system."""
    try:
        rag_system = get_rag_system()
        response = rag_system.query_documents(query)
        if not response or str(response).strip() == "":
            return None
        return str(response)
    except Exception as e:
        st.error(f"Error retrieving resources: {str(e)}")
        return None

def generate_chat_response(client, messages):
    """Generate chat response using Azure OpenAI"""
    try:
        last_message = messages[-1]["content"]
        rag_response = get_relevant_resources(last_message)
        
        base_system_prompt = st.session_state.system_prompt
        if rag_response:
            system_prompt = (
                f"{base_system_prompt}\n\n"
                f"Based on our knowledge base, here is relevant information to help answer:\n{rag_response}\n\n"
                f"Please use this information to provide a detailed, accurate response. "
                f"If the information is relevant, incorporate it naturally into your response."
            )
        else:
            system_prompt = base_system_prompt
            
        chat_messages = [{"role": "system", "content": system_prompt}]
        chat_messages.extend(messages)
        
        response = client.chat.completions.create(
            model=AZURE_CONFIG["model"],
            messages=chat_messages,
            temperature=AZURE_CONFIG["temperature"],
            max_tokens=AZURE_CONFIG["max_tokens"]
        )
        
        if response.choices:
            return response.choices[0].message.content
            
        return "I apologize, but I couldn't generate a response. Please try again."
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "I apologize, but I encountered an error. Please try again."

def transform_links_to_buttons(text):
    """Transform markdown links in text to Streamlit buttons.
    
    Args:
        text (str): Text containing markdown links
        
    Returns:
        tuple: (transformed_text, has_links) where transformed_text has links removed 
        and has_links indicates if any links were found
    """
    pattern = r'\[(.*?)\]\((.*?)\)'
    links = re.findall(pattern, text)
    transformed_text = re.sub(pattern, '', text)
    return transformed_text.strip(), links

@st.dialog("Library", width="large")
def open_link_dialog(title, url):
    """Dialog for displaying link content."""
    # Display the iframe with the content
    iframe_style = """
        <style>
            iframe {
                width: 100%;
                height: 600px;
                border: none;
                border-radius: 8px;
            }
        </style>
    """
    st.markdown(iframe_style, unsafe_allow_html=True)
    
    iframe_html = f"""
        <iframe src="{url}" title="{title}"></iframe>
    """
    st.markdown(iframe_html, unsafe_allow_html=True)

def handle_chat_input(messages_container, client, prompt):
    """Handle chat input and responses"""
    if not prompt or prompt.strip() == "":
        return
        
    try:
        with messages_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        
        st.session_state.stress_messages.append({"role": "user", "content": prompt})
        
        with messages_container:
            with st.chat_message("assistant"):
                with st.spinner(""):
                    messages = []
                    messages.extend(st.session_state.stress_messages)
                    assistant_message = generate_chat_response(client, messages)
                
                if assistant_message and assistant_message.strip():
                    message_text, links = transform_links_to_buttons(assistant_message)
                    message_id = int(time.time() * 1000)
                    
                    if 'message_links' not in st.session_state:
                        st.session_state.message_links = {}
                    st.session_state.message_links[message_id] = links
                    
                    if message_text:
                        st.write(message_text)
                    
                    if links:
                        cols = st.columns([1] * min(len(links), 3))
                        for idx, (link_text, link_url) in enumerate(links):
                            col_idx = idx % len(cols)
                            with cols[col_idx]:
                                button_key = f"link_{message_id}_{idx}"
                                if st.button(f"{link_text}", key=button_key, use_container_width=True):
                                    open_modal_dialog(link_text, link_url)
                    
                    st.session_state.stress_messages.append({
                        "role": "assistant",
                        "content": message_text,
                        "message_id": message_id
                    })
                else:
                    st.error("I apologize, but I couldn't generate a proper response. Please try again.")
        
        st.rerun()
    except Exception as e:
        st.error(f"Error in chat handling: {str(e)}")
        with messages_container:
            with st.chat_message("assistant"):
                st.error("I apologize, but I encountered an error. Please try again.")

def render_stress_reduction_section(client=None):
    """Render stress reduction chat interface."""
    st.markdown("### Stress Management Chat")
    
    if client is None:
        client = get_azure_client()
    
    if "stress_messages" not in st.session_state:
        st.session_state.stress_messages = []
    if "message_links" not in st.session_state:
        st.session_state.message_links = {}
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    
    header_col1, header_col2 = st.columns([6, 1])
    with header_col2:
        if st.button("Restart Chat", key="stress_restart_button"):
            st.session_state.stress_messages = []
            st.session_state.chat_started = False
            st.rerun()
    
    with st.expander("Configure Chat Agent", expanded=not st.session_state.chat_started):
        st.text_area(
            "Customize the agent's behavior:",
            value=st.session_state.system_prompt,
            key="prompt_editor",
            height=150,
            help="Edit this prompt to customize how the agent interacts"
        )
        
        if not st.session_state.chat_started:
            if st.button("Start Chat", type="primary", key="stress_start_button"):
                st.session_state.system_prompt = st.session_state.prompt_editor
                st.session_state.chat_started = True
                st.session_state.stress_messages.append({
                    "role": "assistant",
                    "content": "Hello! I'm here to help you manage stress and develop effective coping strategies. How are you feeling today?"
                })
                st.rerun()
    
    if st.session_state.chat_started:
        messages_container = st.container()
        
        with messages_container:
            for message in st.session_state.stress_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if message["role"] == "assistant" and "message_id" in message:
                        message_links = st.session_state.message_links.get(message["message_id"], [])
                        if message_links:
                            cols = st.columns([1] * min(len(message_links), 3))
                            for idx, (link_text, link_url) in enumerate(message_links):
                                col_idx = idx % len(cols)
                                with cols[col_idx]:
                                    button_key = f"link_{message['message_id']}_{idx}"
                                    if st.button(f"🔗 {link_text}", key=button_key, use_container_width=True):
                                        open_modal_dialog(link_text, link_url)
        
        prompt = st.chat_input("Type your message here...", key="stress_chat_input")
        if prompt:
            handle_chat_input(messages_container, client, prompt)

if __name__ == "__main__":
    render_stress_reduction_section() 