import streamlit as st
import requests
from datetime import datetime

def init_session_state():
    """Initialize session state variables"""
    if 'user_token' not in st.session_state:
        st.session_state.user_token = None
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False

def login_user(username, password):
    """Authenticate user and get token"""
    try:
        # Replace with your actual API endpoint
        response = requests.post(
            "YOUR_API_ENDPOINT/login",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('token'), None
        else:
            return None, "Invalid credentials. Please try again."
            
    except Exception as e:
        return None, f"Login failed: {str(e)}"

def render_login_screen():
    """Render the login screen"""
    init_session_state()
    
    if st.session_state.is_authenticated:
        return True
    
    st.markdown("### Welcome to Otto")
    st.markdown("Please login to continue")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                token, error = login_user(username, password)
                if token:
                    st.session_state.user_token = token
                    st.session_state.is_authenticated = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(error)
            else:
                st.error("Please enter both username and password")
    
    st.markdown("---")
    if st.button("Don't have an account? Sign up"):
        st.session_state.show_signup = True
    
    return False

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