import streamlit as st
from datetime import datetime
from templates import PROMPTS, TRANSCRIPTS


def render_prompt_section():
    """Render prompt selection and input section"""
    st.markdown("#### Select Prompt Template")
    
    use_custom_api = st.checkbox("Use Custom API for Summary Generation")
    api_config = None
    
    if use_custom_api:
        with st.expander("API Configuration"):
            api_url = st.text_input("API Endpoint URL")
            bearer_token = st.text_input("Bearer Token", type="password")
            api_body = st.text_area(
                "Enter API request body (JSON):",
                height=150
            )
            api_config = {
                "url": api_url,
                "token": bearer_token,
                "body": api_body
            }
        prompt = None
    else:
        # Only show OpenAI-specific prompt options when not using custom API
        prompt_choice = st.radio(
            "Choose a prompt template or create custom:",
            ["Select Predefined", "Create Custom"]
        )
        
        if prompt_choice == "Select Predefined":
            selected_prompt = st.selectbox(
                "Select a predefined prompt:",
                list(PROMPTS.keys())
            )
            prompt = PROMPTS[selected_prompt]
            st.markdown("##### Selected Prompt:")
            st.markdown(f"""<div class="prompt-box">{prompt}</div>""", unsafe_allow_html=True)
        else:
            prompt = st.text_area(
                "Enter custom prompt:",
                height=150
            )
    
    return prompt, api_config

def render_transcript_section():
    """Render transcript selection and input section"""
    st.markdown("#### Session Transcript")
    transcript_choice = st.radio(
        "Choose a transcript source:",
        ["Select Example", "Input New"]
    )
    
    if transcript_choice == "Select Example":
        selected_transcript = st.selectbox(
            "Select an example transcript:",
            list(TRANSCRIPTS.keys())
        )
        transcript = TRANSCRIPTS[selected_transcript]
        # Remove preview - transcript will only be shown in results
    else:
        transcript = st.text_area(
            "Enter or paste the session transcript:",
            height=200
        )
    return transcript

def display_conversation(transcript):
    """Display conversation in a chat-like interface"""
    # Create a container with custom styling
    st.markdown("""
        <style>
        .chat-container {
            padding: 10px;
            border-radius: 10px;
            background-color: #f5f5f5;
            margin: 10px 0;
        }
        .message {
            padding: 10px;
            margin: 5px 0;
            border-radius: 15px;
            max-width: 80%;
            color: black;
        }
        .therapist {
            background-color: #e3f2fd;
            margin-right: 20%;
        }
        .client {
            background-color: #f0f4c3;
            margin-left: 20%;
        }
        .observation {
            font-style: italic;
            color: #666;
            font-size: 0.9em;
            margin: 2px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Split transcript into lines and process each line
        lines = transcript.strip().split('\n')
        speakers = set()
        conversation_pairs = []
        current_speaker = None
        
        # First pass: Identify unique speakers and conversation structure
        for line in lines:
            line = line.strip()
            if not line or (line.startswith('[') and line.endswith(']')):
                continue
                
            # Check if line starts with a potential speaker indicator
            colon_split = line.split(':', 1)
            if len(colon_split) == 2:
                potential_speaker = colon_split[0].strip()
                # Add to speakers if it looks like a speaker (short name/title)
                if len(potential_speaker.split()) <= 3:
                    speakers.add(potential_speaker.lower())
        
        # Second pass: Process the conversation
        buffer = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Handle observations
            if line.startswith('[') and line.endswith(']'):
                st.markdown(f'<div class="observation">{line}</div>', unsafe_allow_html=True)
                continue
            
            message = line
            speaker = None
            
            # Check if line starts with known speaker
            colon_split = line.split(':', 1)
            if len(colon_split) == 2 and colon_split[0].strip().lower() in speakers:
                speaker = colon_split[0].strip().lower()
                message = colon_split[1].strip()
            else:
                # If no explicit speaker, determine based on conversation flow
                if not current_speaker:
                    # First speaker is typically the therapist
                    speaker = list(speakers)[0] if speakers else "speaker1"
                else:
                    # Alternate speakers if no explicit indication
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
                    st.markdown(f'<div class="observation">{observation}</div>', unsafe_allow_html=True)
            
            # Determine CSS class (first speaker is therapist, second is client)
            speaker_list = list(speakers) if speakers else ["speaker1", "speaker2"]
            css_class = "therapist" if speaker == speaker_list[0] else "client"
            
            # Display the message
            st.markdown(f'<div class="message {css_class}">{message}</div>', unsafe_allow_html=True)
            
            current_speaker = speaker
            
        st.markdown('</div>', unsafe_allow_html=True)

def render_results(transcript, summary, api_config=None):
    """Render analysis results"""
    st.markdown("### Analysis Results")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Original Transcript")
        display_conversation(transcript)
    
    with col2:
        st.markdown("#### Generated Summary")
        if api_config:
            st.info("Using custom API for summary generation")
        
        if summary is None or isinstance(summary, dict) and 'error' in summary:
            st.error("Unable to generate summary. Please try again or contact support if the issue persists.")
        else:
            st.markdown(f"""
                <div class="summary-box">
                    {summary}
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### Feedback")
            quality_rating = st.select_slider(
                "Summary Quality",
                options=["Poor", "Fair", "Good", "Very Good", "Excellent"],
                value="Good"
            )
            
            if st.button("Save Analysis"):
                st.success("Analysis saved successfully!")
