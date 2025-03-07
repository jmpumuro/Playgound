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

def open_feedback_modal(title: str, url: str):
    """A specialized modal dialog for displaying the feedback form.
    
    This version uses maximum width and height and doesn't include a Done button.
    
    Args:
        title (str): The title of the feedback form
        url (str): The URL to the Google Sheet
    """
    
    # Use a larger dialog size
    @st.dialog(title=title)
    def show_feedback_dialog():
        # Add custom CSS to make the dialog and iframe as large as possible
        st.markdown(
            """
            <style>
                /* Make the dialog larger */
                [data-testid="stDialog"] {
                    max-width: 90vw !important;
                    width: 90vw !important;
                }
                
                /* Make the dialog content area larger */
                [data-testid="stDialog"] > div:first-child {
                    max-width: 100% !important;
                    width: 100% !important;
                    height: 90vh !important;
                    max-height: 90vh !important;
                }
                
                /* Style the iframe */
                iframe {
                    width: 100%;
                    height: 85vh;
                    border: none;
                    border-radius: 8px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Display the Google Sheet in an iframe
        st.markdown(
            f'<iframe src="{url}" title="{title}"></iframe>',
            unsafe_allow_html=True
        )
    
    # Call the dialog function
    show_feedback_dialog() 