from azure_client import generate_summary
import streamlit as st
from datetime import datetime
from templates import PROMPTS, TRANSCRIPTS
import base64
import requests
import json
from reflection_template import REFLECTION_PROMPTS
import auth


def render_prompt_section():
    """Render prompt selection and input section"""
    st.markdown("###  Configure Summary Generation")
    
    st.markdown("#### Prompt Selection")
    prompt_choice = st.radio(
        "Choose your prompt:",
        ["Use Template", "Write Custom"],
        help="Select a pre-defined template or write your own custom prompt"
    )
    
    if prompt_choice == "Use Template":
        selected_prompt = st.selectbox(
            "Select a template:",
            list(PROMPTS.keys()),
            help="Choose from our curated prompt templates"
        )
        prompt = PROMPTS[selected_prompt]
        with st.expander("View Selected Prompt"):
            st.markdown(f"""<div class="prompt-box">{prompt}</div>""", unsafe_allow_html=True)
    else:
        prompt = st.text_area(
            "Write your custom prompt:",
            placeholder="Enter instructions for the AI summarizer...",
            height=150
        )
    
    return prompt, None  # Return None for api_config since we're not using custom API

def render_transcript_section():
    """Render transcript selection and input section"""
    st.markdown("###  Provide Session Transcript")
    
    transcript_choice = st.radio(
        "Choose transcript source:",
        ["Load Example", "Enter New", "Upload File"],
        help="Select an example transcript, input your own, or upload a file"
    )
    
    if transcript_choice == "Load Example":
        selected_transcript = st.selectbox(
            "Select an example:",
            list(TRANSCRIPTS.keys()),
            help="Choose from our sample transcripts"
        )
        transcript = TRANSCRIPTS[selected_transcript]
    elif transcript_choice == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload transcript file",
            type=["txt"],
            help="Upload a text file containing the session transcript"
        )
        if uploaded_file is not None:
            try:
                transcript = uploaded_file.getvalue().decode("utf-8")
            except Exception as e:
                st.error("Error reading file. Please ensure it's a valid text file.")
                transcript = None
        else:
            transcript = None
    else:
        transcript = st.text_area(
            "Enter session transcript:",
            placeholder="Paste your session transcript here...",
            height=200
        )
    return transcript

def display_conversation(transcript):
    """Display conversation in a chat-like interface"""
    # Create a container div with custom HTML/CSS
    html_content = ['<div class="chat-container">']
    
    # Split transcript into lines and process each line
    lines = transcript.strip().split('\n')
    speakers = set()
    current_speaker = None
    
    # First pass: Identify unique speakers
    for line in lines:
        line = line.strip()
        if not line or (line.startswith('[') and line.endswith(']')):
            continue
        colon_split = line.split(':', 1)
        if len(colon_split) == 2:
            potential_speaker = colon_split[0].strip()
            if len(potential_speaker.split()) <= 3:
                speakers.add(potential_speaker.lower())
    
    # Second pass: Process the conversation
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Handle observations
        if line.startswith('[') and line.endswith(']'):
            html_content.append(f'<div class="observation">{line}</div>')
            continue
        
        message = line
        speaker = None
        
        # Check if line starts with known speaker
        colon_split = line.split(':', 1)
        if len(colon_split) == 2 and colon_split[0].strip().lower() in speakers:
            speaker = colon_split[0].strip().lower()
            message = colon_split[1].strip()
        else:
            if not current_speaker:
                speaker = list(speakers)[0] if speakers else "speaker1"
            else:
                speaker_list = list(speakers) if speakers else ["speaker1", "speaker2"]
                current_idx = speaker_list.index(current_speaker)
                speaker = speaker_list[(current_idx + 1) % len(speaker_list)]
        
        # Extract any inline observations
        observation = ""
        if '[' in message and ']' in message:
            start = message.find('[')
            end = message.find(']') + 1
            observation = message[start:end]
            message = message.replace(observation, '').strip()
            if observation:
                html_content.append(f'<div class="observation">{observation}</div>')
        
        # Determine CSS class
        speaker_list = list(speakers) if speakers else ["speaker1", "speaker2"]
        css_class = "therapist" if speaker == speaker_list[0] else "client"
        
        # Add message to HTML content
        html_content.append(f'<div class="message {css_class}">{message}</div>')
        
        current_speaker = speaker
    
    # Close the container div
    html_content.append('</div>')
    
    # Render all content at once
    st.markdown('\n'.join(html_content), unsafe_allow_html=True)

def render_results(transcript, summary, api_config=None):
    """Render analysis results"""
    st.markdown("### Analysis Results")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        tab1, tab2 = st.tabs(["Conversation View", "Raw Transcript"])
        
        with tab1:
            display_conversation(transcript)
            
        with tab2:
            st.text_area("Raw Transcript", value=transcript, height=400, disabled=True)
    
    with col2:
        st.markdown("#### Generated Summary")
        
        if summary is None or isinstance(summary, dict) and 'error' in summary:
            st.error("Unable to generate summary. Please try again or contact support if the issue persists.")
        else:
            st.markdown(f"""
                <div class="summary-box">
                    {summary}
                </div>
            """, unsafe_allow_html=True)
            
            # Replace feedback section with reset button
            if st.button("Reset", type="primary"):
                st.session_state.clear()
                st.rerun()

def create_reflection_entry(token, mood):
    """Create a new reflection entry"""
    url = "https://conciergesvc-bowie.sondermind.biz/api/v1/reflection/entries"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"  # Added content type header
    }
    payload = {"overall_mood": mood}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        
        if response.content:  # Check if response has content
            return response.json()
        return {"status": "success"}  # Return default response if no content
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
    
    # Check if user is authenticated
    if not auth.render_login_section():
        return

    # Choose reflection mode
    reflection_mode = st.radio(
        "Choose your reflection mode:",
        ["Chat with Otto", "Freeform Journaling"],
        help="Select how you'd like to reflect on your day"
    )
    
    if reflection_mode == "Chat with Otto":
        # Add prompt configuration
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
        
        # Initialize session in session state if not exists
        if "reflection_session" not in st.session_state:
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

        # Display chat messages
        messages_container = st.container()
        
        # Display existing messages
        with messages_container:
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Only show chat input if session is initialized
        if "reflection_session" in st.session_state:
            prompt = st.chat_input("Type your message here...")
            
            if prompt:
                # Display user message immediately
                with messages_container:
                    with st.chat_message("user"):
                        st.markdown(prompt)
                
                # Add user message to history
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                
                # Get and display assistant response
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
        
        # Update the Generate Summary button section
        if st.button("Generate Reflection Summary", type="primary"):
            with st.spinner("Analyzing your reflection..."):
                # Check if there are any user messages
                user_messages = [msg for msg in st.session_state.chat_messages if msg["role"] == "user"]
                if not user_messages:
                    st.warning("No user input found. Please share your thoughts with Otto before generating a summary.")
                    return
                
                # Format the entire conversation history
                conversation = []
                for msg in st.session_state.chat_messages:
                    role = "Otto" if msg["role"] == "assistant" else "User"
                    conversation.append(f"{role}: {msg['content']}")
                
                content = "\n".join(conversation)
                
                # Generate summary using Azure OpenAI
                summary = generate_summary(client, summary_prompt, content)
                
                if not summary:
                    st.error("Failed to generate summary. Please try again.")
                    return
                
                # Display summary
                st.markdown("#### Summary")
                st.markdown(summary)
    
    else:  # Freeform Journaling
        # Configuration for freeform journaling
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
            
        st.markdown("#### Journal Entry")
        journal_entry = st.text_area(
            "Write about your day:",
            placeholder="Take a moment to reflect on your day...",
            height=300
        )

        # Add summary generation button for journal entry
        if st.button("Generate Journal Summary", type="primary"):
            if not journal_entry:
                st.warning("Please write your journal entry before generating a summary.")
                return
                
            with st.spinner("Analyzing your journal entry..."):
                # Generate summary using Azure OpenAI
                summary = generate_summary(client, summary_prompt, journal_entry)
                
                if not summary:
                    st.error("Failed to generate summary. Please try again.")
                    return
                
                # Display summary components
                st.markdown("#### Summary")
                st.markdown(summary)
