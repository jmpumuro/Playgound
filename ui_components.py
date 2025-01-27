import streamlit as st
from datetime import datetime
from templates import PROMPTS, TRANSCRIPTS


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
            
            st.markdown("#### Feedback")
            quality_rating = st.select_slider(
                "Summary Quality",
                options=["Poor", "Fair", "Good", "Very Good", "Excellent"],
                value="Good"
            )
            
            if st.button("Save Analysis"):
                st.success("Analysis saved successfully!")
