import streamlit as st

def open_modal_dialog(title: str, url: str, height: int = 600):
    """A reusable modal dialog component for displaying content in an iframe.
    
    Args:
        title (str): The title of the content
        url (str): The URL to display in the iframe
        height (int, optional): Height of the iframe in pixels. Defaults to 600.
    """
    
    @st.dialog(title="Library", width="large")
    def show_dialog():
        iframe_style = f"""
            <style>
                iframe {{
                    width: 100%;
                    height: {height - 50}px;
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
        
        # Add submit button at the bottom
        if st.button("Done", type="primary", use_container_width=True):
            # Set flag to generate summary on next rerun
            st.session_state.generate_summary = True
            st.session_state.summary_tool = title
            st.rerun()
    
    # Call the dialog function
    show_dialog() 