import streamlit as st
import requests
import base64

def init_session_state():
    """Initialize session state variables"""
    if 'auth_token' not in st.session_state:
        st.session_state.auth_token = None

def login_user(email, password):
    """Authenticate user and get token"""
    try:
        # Authentication credentials from secrets
        uid = st.secrets["AUTH_UID"]
        secret = st.secrets["AUTH_SECRET"]
        basic = base64.b64encode(f"{uid}:{secret}".encode()).decode()
        
        # Make authentication request
        url = "https://authsvc-bowie.sondermind.biz/oauth/token"
        headers = {"Authorization": f"Basic {basic}"}
        payload = {
            "grant_type": "password",
            "username": email,
            "password": password
        }
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token"), None
        else:
            return None, "Invalid credentials. Please try again."
            
    except Exception as e:
        return None, f"Authentication failed: {str(e)}"

def render_auth_header():
    """Render the authentication header with restart and logout buttons"""
    header_col1, header_col2, header_col3 = st.columns([5, 1, 1])
    
    with header_col2:
        if st.button("Restart Chat"):
            # Preserve active tab while clearing chat state
            active_tab = st.session_state.get('active_tab')
            if "reflection_session" in st.session_state:
                del st.session_state.reflection_session
            if "chat_messages" in st.session_state:
                del st.session_state.chat_messages
            if active_tab:
                st.session_state.active_tab = active_tab
            st.rerun()
            
    with header_col3:
        if st.button("Logout"):
            logout_user()
            st.rerun()

def render_login_section():
    """Render login section and handle authentication"""
    init_session_state()
    
    if st.session_state.auth_token:
        render_auth_header()
        return True
        
    st.markdown("#### Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        with st.spinner("Authenticating..."):
            token, error = login_user(email, password)
            if token:
                st.session_state.auth_token = token
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(error)
    
    return False

def logout_user():
    """Log out user by clearing session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def render_signup_form():
    """Render the signup form"""
    st.markdown("### Create an Account")
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if not all([username, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                # Replace with your actual API endpoint
                try:
                    response = requests.post(
                        "YOUR_API_ENDPOINT/signup",
                        json={
                            "username": username,
                            "email": email,
                            "password": password
                        }
                    )
                    
                    if response.status_code == 201:
                        st.success("Account created successfully! Please login.")
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.error("Failed to create account. Please try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if st.button("Already have an account? Login"):
        st.session_state.show_signup = False
        st.rerun() 