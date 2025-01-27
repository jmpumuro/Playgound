CUSTOM_CSS = """
    <style>
    /* Base styles with better contrast */
    .main, label, .stMarkdown p, .stMarkdown div, 
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stRadio > div > label,
    .stExpander > div > div > div > div > label { 
        color: white !important; 
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #2b2b2b !important;
        border: 1px solid #404040 !important;
        color: white !important;
    }
    
    /* Boxes with dark backgrounds */
    .prompt-box, .transcript-box, .summary-box {
        background-color: #2b2b2b;
        border: 1px solid #404040;
        color: white;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    /* Section headers */
    h3 {
        padding: 10px;
        background: #2b2b2b;
        border-left: 4px solid #ff4b4b;
        margin: 20px 0 !important;
        color: white !important;
    }
    
    /* Radio and select containers */
    .stRadio > div {
        background-color: #2b2b2b;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #404040;
    }
    
    /* Chat interface */
    .chat-container {
        padding: 10px;
        border-radius: 10px;
        background-color: #2b2b2b;
        margin: 10px 0;
        border: 1px solid #404040;
        max-height: 500px;  /* Set maximum height to match raw transcript */
        overflow-y: auto;  /* Enable vertical scrolling */
    }
    
    .message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 15px;
        max-width: 80%;
        color: black;
    }
    
    .therapist {
        background-color: #ff4b4b;
        margin-right: 20%;
        color: white;
    }
    
    .client {
        background-color: #4b4b4b;
        margin-left: 20%;
        color: white;
    }
    
    .observation {
        font-style: italic;
        color: #cccccc;
        font-size: 0.9em;
        margin: 2px 0;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        padding: 10px !important;
        font-weight: 500;
        background-color: #ff4b4b !important;
        color: white !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #2b2b2b !important;
        border: 1px solid #404040 !important;
    }
    
    /* Info messages */
    .stAlert > div {
        color: white !important;
        background-color: #2b2b2b !important;
        border: 1px solid #404040 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #2b2b2b !important;
        color: white !important;
    }
    
    .streamlit-expanderContent {
        background-color: #2b2b2b !important;
        color: white !important;
    }
    </style>
"""