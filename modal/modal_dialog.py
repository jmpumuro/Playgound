import streamlit as st

@st.dialog("Library", width="large")
def open_modal_dialog(title: str, url: str, height: int = 600):
    """A reusable modal dialog component for displaying content in an iframe.
    
    Args:
        title (str): The title of the content
        url (str): The URL to display in the iframe
        height (int, optional): Height of the iframe in pixels. Defaults to 600.
    """
    iframe_style = f"""
        <style>
            iframe {{
                width: 100%;
                height: {height}px;
                border: none;
                border-radius: 8px;
            }}
        </style>
    """
    st.markdown(iframe_style, unsafe_allow_html=True)
    
    iframe_html = f"""
        <iframe src="{url}" title="{title}"></iframe>
    """
    st.markdown(iframe_html, unsafe_allow_html=True) 