import streamlit as st
from azure_client import generate_summary
import requests
import json
import auth
from templates.reflection_template import REFLECTION_PROMPTS

def create_reflection_entry(token, mood):
    """Create a new reflection entry"""
    url = "https://conciergesvc-bowie.sondermind.biz/api/v1/reflection/entries"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"overall_mood": mood}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        if response.content:
            return response.json()
        return {"status": "success"}
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating reflection entry: {str(e)}")
        if hasattr(response, 'text'):
            st.error(f"Response text: {response.text}")
        return None

def start_reflection_session(token):
    """Start a new reflection session"""
    url = "https://conciergesvc-bowie.sondermind.biz/api/v1/reflection/sessions/start"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        if response.content:
            data = response.json()
            
            if isinstance(data, dict):
                if 'data' in data and isinstance(data['data'], dict):
                    session_id = data['data'].get('id')
                elif 'id' in data:
                    session_id = data['id']
                else:
                    session_id = None
            else:
                session_id = None
                
            if session_id:
                return {"id": session_id}
            return data
            
        return {"status": "success"}
    except requests.exceptions.RequestException as e:
        st.error(f"Error starting reflection session: {str(e)}")
        if hasattr(response, 'text'):
            st.error(f"Response text: {response.text}")
        return None

def send_chat_message(token, session_id, message):
    """Send a message to the chat session"""
    url = f"https://conciergesvc-bowie.sondermind.biz/api/v1/reflection/sessions/{session_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"message": message}
    
    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        accumulated_message = ""
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if 'm' in data:
                    accumulated_message += data['m']
        
        return {"m": accumulated_message}
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Error sending chat message: {str(e)}"
        if hasattr(response, 'text'):
            error_msg += f"\nResponse text: {response.text}"
        st.error(error_msg)
        return {"m": "I'm having trouble connecting right now. Please try again."}

def render_reflection_section(client):
    """Render the reflection section UI"""
    st.markdown("### Daily Reflection")
    
    if not auth.render_login_section():
        return

    reflection_mode = st.radio(
        "Choose your reflection mode:",
        ["Chat with Otto", "Freeform Journaling"],
        help="Select how you'd like to reflect on your day"
    )
    
    if reflection_mode == "Chat with Otto":
        render_chat_mode(client)
    else:
        render_journal_mode(client)

def render_chat_mode(client):
    """Render the chat interface for reflection"""
    with st.expander("Configure Summary Generation"):
        prompt_type = st.selectbox(
            "Select summary template:",
            list(REFLECTION_PROMPTS.keys()),
            index=0
        )
        summary_prompt = st.text_area(
            "Customize summary generation prompt:",
            value=REFLECTION_PROMPTS[prompt_type],
            height=100
        )
    
    if "reflection_session" not in st.session_state:
        initialize_chat_session()
    
    messages_container = st.container()
    
    with messages_container:
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    handle_chat_input(messages_container, client, summary_prompt)

def render_journal_mode(client):
    """Render the journaling interface for reflection"""
    with st.expander("Configure Summary Generation"):
        prompt_type = st.selectbox(
            "Select summary template:",
            list(REFLECTION_PROMPTS.keys()),
            index=list(REFLECTION_PROMPTS.keys()).index("Journal Summary"),
            help="Choose a template for analyzing your journal entry"
        )
        summary_prompt = st.text_area(
            "Customize summary generation prompt:",
            value=REFLECTION_PROMPTS[prompt_type],
            height=100
        )
        
    st.markdown("#### Journal Entry")
    journal_entry = st.text_area(
        "Write about your day:",
        placeholder="Take a moment to reflect on your day...",
        height=300
    )

    if st.button("Generate Journal Summary", type="primary"):
        handle_journal_summary(journal_entry, client, summary_prompt)

def initialize_chat_session():
    """Initialize a new chat session"""
    with st.spinner("Initializing chat..."):
        entry = create_reflection_entry(st.session_state.auth_token, 0.0)
        if entry is None:
            st.error("Failed to create reflection entry")
            return
        
        session = start_reflection_session(st.session_state.auth_token)
        if session is None:
            st.error("Failed to start reflection session")
            return
        
        session_id = session.get('id')
        if not session_id:
            st.error("No session ID received in response data")
            st.error(f"Response data: {session}")
            return
        
        st.session_state.reflection_session = session_id
        st.session_state.chat_messages = [{
            "role": "assistant",
            "content": "Hi, I'm Otto. I'm here to help you reflect on your day. How are you feeling?"
        }]
        st.rerun()

def handle_chat_input(messages_container, client, summary_prompt):
    """Handle chat input and responses"""
    if "reflection_session" in st.session_state:
        prompt = st.chat_input("Type your message here...")
        
        if prompt:
            process_chat_message(prompt, messages_container)
            
        if st.button("Generate Reflection Summary", type="primary"):
            generate_chat_summary(client, summary_prompt)

def process_chat_message(prompt, messages_container):
    """Process a new chat message"""
    with messages_container:
        with st.chat_message("user"):
            st.markdown(prompt)
    
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    
    with messages_container:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with response_placeholder:
                with st.spinner(""):
                    response = send_chat_message(
                        st.session_state.auth_token,
                        st.session_state.reflection_session,
                        prompt
                    )
            
            if isinstance(response, dict) and 'm' in response:
                assistant_message = response['m']
                response_placeholder.markdown(assistant_message)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
    
    st.rerun()

def generate_chat_summary(client, summary_prompt):
    """Generate a summary of the chat conversation"""
    with st.spinner("Analyzing your reflection..."):
        user_messages = [msg for msg in st.session_state.chat_messages if msg["role"] == "user"]
        if not user_messages:
            st.warning("No user input found. Please share your thoughts with Otto before generating a summary.")
            return
        
        conversation = []
        for msg in st.session_state.chat_messages:
            role = "Otto" if msg["role"] == "assistant" else "User"
            conversation.append(f"{role}: {msg['content']}")
        
        content = "\n".join(conversation)
        summary = generate_summary(client, summary_prompt, content)
        
        if not summary:
            st.error("Failed to generate summary. Please try again.")
            return
        
        st.markdown("#### Summary")
        st.markdown(summary)

def handle_journal_summary(journal_entry, client, summary_prompt):
    """Generate a summary for journal entry"""
    if not journal_entry or journal_entry.strip() == "":
        st.warning("Please write your journal entry before generating a summary.")
    else:
        with st.spinner("Analyzing your journal entry..."):
            summary = generate_summary(client, summary_prompt, journal_entry)
            
            if not summary:
                st.error("Failed to generate summary. Please try again.")
                return
            
            st.markdown("#### Summary")
            st.markdown(summary) 