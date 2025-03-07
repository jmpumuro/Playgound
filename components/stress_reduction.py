from typing import List, Tuple, Optional, Dict, Any
import streamlit as st
from azure_client import init_azure_openai
from config import AZURE_CONFIG
from rag import get_rag_system
from templates.stress_reduction_prompts import DEFAULT_SYSTEM_PROMPT
from templates.link_injector import inject_tool_link, get_tool_link
from templates.stress_reduction_summary import get_tool_summary_prompt, get_conversation_summary_prompt
from modal.modal_dialog import open_modal_dialog
from components.document_manager import render_document_manager
import time
import re
import webbrowser
from openai.types.chat import ChatCompletion

class ChatMessage:
    def __init__(self, role: str, content: str, message_id: Optional[int] = None):
        self.role = role
        self.content = content
        self.message_id = message_id

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

class StressReductionChat:
    def __init__(self):
        self.client = self._initialize_azure_client()
        self._initialize_session_state()

    def _initialize_azure_client(self):
        """Initialize and return Azure OpenAI client"""
        if 'azure_client' not in st.session_state:
            client = init_azure_openai()
            if client is None:
                st.error("Failed to initialize Azure OpenAI client. Please check your credentials.")
                st.stop()
            st.session_state.azure_client = client
        return st.session_state.azure_client

    def _initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if "stress_messages" not in st.session_state:
            st.session_state.stress_messages = []
        if "message_links" not in st.session_state:
            st.session_state.message_links = {}
        if "system_prompt" not in st.session_state:
            st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT
        if "chat_started" not in st.session_state:
            st.session_state.chat_started = False

    def _get_relevant_resources(self, query: str) -> Optional[str]:
        """Query RAG system for relevant resources"""
        try:
            rag_system = get_rag_system()
            response = rag_system.query_documents(query)
            return str(response) if response and str(response).strip() else None
        except Exception as e:
            st.error(f"Error retrieving resources: {str(e)}")
            return None

    def _create_system_prompt(self, user_query: str) -> str:
        """Create system prompt with RAG context if available"""
        rag_response = self._get_relevant_resources(user_query)
        base_prompt = st.session_state.system_prompt
        
        if not rag_response:
            return base_prompt
            
        return (
            f"{base_prompt}\n\n"
            f"Based on our knowledge base, here is relevant information to help answer:\n{rag_response}\n\n"
            f"Please use this information to provide a detailed, accurate response. "
            f"If the information is relevant, incorporate it naturally into your response."
        )

    def _generate_chat_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Generate response using Azure OpenAI"""
        try:
            system_prompt = self._create_system_prompt(messages[-1]["content"])
            chat_messages = [{"role": "system", "content": system_prompt}] + messages
            
            response: ChatCompletion = self.client.chat.completions.create(
                model=AZURE_CONFIG["model"],
                messages=chat_messages,
                temperature=AZURE_CONFIG["temperature"],
                max_tokens=AZURE_CONFIG["max_tokens"]
            )
            
            return response.choices[0].message.content if response.choices else None
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return None

    def _parse_markdown_links(self, text: str) -> Tuple[str, List[Tuple[str, str]]]:
        """Extract markdown links from text"""
        pattern = r'\[(.*?)\]\((.*?)\)'
        links = re.findall(pattern, text)
        transformed_text = re.sub(pattern, '', text)
        return transformed_text.strip(), links

    def _render_message_links(self, message_id: int, links: List[Tuple[str, str]]):
        """Render links as buttons in columns"""
        if not links:
            return
            
        cols = st.columns([1] * min(len(links), 3))
        for idx, (link_text, link_url) in enumerate(links):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                if st.button(f"{link_text}", key=f"link_{message_id}_{idx}", use_container_width=True):
                    # Set modal state to True when opening
                    st.session_state.modal_open = True
                    st.session_state.current_tool = link_text
                    open_modal_dialog(
                        title="Link",
                        url=link_url,
                        height=700
                    )

    def _generate_tool_summary(self, tool_name: str):
        """Generate a summary of the conversation after tool usage"""
        summary_prompt = get_tool_summary_prompt(tool_name)
        
        # Create a copy of messages for summary generation
        messages_for_summary = [
            {"role": "user", "content": summary_prompt}
        ]
        
        try:
            response = self._generate_chat_response(messages_for_summary)
            if response:
                # Store the summary in session state
                if "tool_summaries" not in st.session_state:
                    st.session_state.tool_summaries = []
                st.session_state.tool_summaries.append({
                    "tool": tool_name,
                    "summary": response,
                    "timestamp": time.time()
                })
        except Exception as e:
            st.error(f"Error generating summary: {str(e)}")

    def _handle_user_message(self, messages_container, prompt: str):
        """Process user message and generate response"""
        if not prompt.strip():
            return

        # Remove feedback dialog flag completely when user sends a message
        if "show_feedback_dialog" in st.session_state:
            del st.session_state.show_feedback_dialog

        # Display user message
        with messages_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        st.session_state.stress_messages.append({"role": "user", "content": prompt})
        
        # Generate and display assistant response
        with messages_container:
            with st.chat_message("assistant"):
                with st.spinner(""):
                    response = self._generate_chat_response(st.session_state.stress_messages)
                
                if response and response.strip():
                    self._process_assistant_response(response)
                else:
                    st.error("I apologize, but I couldn't generate a proper response. Please try again.")

        st.rerun()

    def _process_assistant_response(self, response: str):
        """Process and display assistant's response with links"""
        try:
            # First inject any tool links
            response_with_links = inject_tool_link(response)
            
            # Then parse any remaining markdown links
            message_text, links = self._parse_markdown_links(response_with_links)
            message_id = int(time.time() * 1000)
            
            if message_text:
                st.markdown(message_text)
            
            if links:
                self._render_message_links(message_id, links)
                st.session_state.message_links[message_id] = links
            
            st.session_state.stress_messages.append({
                "role": "assistant",
                "content": message_text,
                "message_id": message_id
            })
        except Exception as e:
            st.error("I apologize, but I encountered an issue processing the response. Let me try a different approach.")

    def render_interface(self):
        """Render the main chat interface"""
        # Handle summary generation if flag is set
        if st.session_state.get("generate_summary"):
            tool_name = st.session_state.get("summary_tool", "the tool")
            summary_prompt = get_conversation_summary_prompt()
            
            # Generate response without adding user message to chat history
            temp_messages = st.session_state.stress_messages.copy()
            temp_messages.append({"role": "user", "content": summary_prompt})
            response = self._generate_chat_response(temp_messages)
            
            if response:
                # Process the response using existing method to handle links
                with st.chat_message("assistant"):
                    self._process_assistant_response(f"**Conversation Summary:**\n\n{response}")
            
            # Clear the flags
            st.session_state.generate_summary = False
            st.session_state.summary_tool = None
            # Also clear feedback dialog flag
            if "show_feedback_dialog" in st.session_state:
                del st.session_state.show_feedback_dialog
            st.rerun()
        
        # Define the feedback dialog function - only used when explicitly called
        @st.dialog("Feedback Form", width="large")
        def show_feedback_dialog():
            feedback_url = "https://docs.google.com/spreadsheets/d/1ZRIkMOIKR4XoI5CbXtvbfAruFuSdxaKDwD41nrybd7c/edit?usp=sharing"
            
            # Add custom CSS to make the iframe as large as possible
            st.markdown(
                """
                <style>
                    iframe {
                        width: 100%;
                        height: 80vh;
                        border: none;
                        border-radius: 8px;
                    }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            # Display the Google Sheet in an iframe
            st.markdown(
                f'<iframe src="{feedback_url}" title="Feedback Form"></iframe>',
                unsafe_allow_html=True
            )
            
            # Add a button to explicitly close the dialog
            if st.button("Close", type="primary"):
                # Remove the flag completely instead of setting to False
                if "show_feedback_dialog" in st.session_state:
                    del st.session_state.show_feedback_dialog
                st.rerun()
        
        st.markdown("### Stress Management Agent")
        
        # Create tabs for chat and document management
        chat_tab, docs_tab = st.tabs(["Chat Interface", "Knowledge Base"])
        
        with chat_tab:
            # Header with restart button and feedback button
            header_col1, header_col2, header_col3 = st.columns([6, 1, 1])
            with header_col2:
                if st.button("Restart Chat", key="stress_restart_button"):
                    st.session_state.stress_messages = []
                    st.session_state.chat_started = False
                    # Remove the feedback dialog flag completely
                    if "show_feedback_dialog" in st.session_state:
                        del st.session_state.show_feedback_dialog
                    st.rerun()
            with header_col3:
                # Display feedback form in a modal dialog
                if st.button("Feedback", key="stress_feedback_button"):
                    # Only now do we check and show the feedback dialog
                    st.session_state.show_feedback_dialog = True
                    show_feedback_dialog()
            
            self._render_configuration_section()
            
            if st.session_state.chat_started:
                self._render_chat_section()
            
        with docs_tab:
            render_document_manager()

    def _render_configuration_section(self):
        """Render the configuration expander"""
        with st.expander("Configure Chat Agent", expanded=not st.session_state.chat_started):
            st.text_area(
                "Customize the agent's behavior:",
                value=st.session_state.system_prompt,
                key="prompt_editor",
                height=150,
                help="Edit this prompt to customize how the agent interacts"
            )
            
            if not st.session_state.chat_started:
                if st.button("Start Chat", type="primary", key="stress_start_button"):
                    self._start_new_chat()

    def _start_new_chat(self):
        """Initialize a new chat session"""
        st.session_state.system_prompt = st.session_state.prompt_editor
        st.session_state.chat_started = True
        # Remove feedback dialog flag completely when starting a new chat
        if "show_feedback_dialog" in st.session_state:
            del st.session_state.show_feedback_dialog
        st.session_state.stress_messages.append({
            "role": "assistant",
            "content": "Hello! I'm here to help you manage stress and develop effective coping strategies. How are you feeling today?"
        })
        st.rerun()

    def _render_chat_section(self):
        """Render the chat messages and input"""
        messages_container = st.container()
        
        with messages_container:
            self._render_chat_history()
        
        # Add auto-scroll functionality
        st.markdown("""
        <script>
            function scrollToBottom() {
                const chatContainer = document.querySelector('.main');
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }
            
            // Scroll when page loads and after content changes
            window.addEventListener('load', scrollToBottom);
            const observer = new MutationObserver(scrollToBottom);
            observer.observe(document.body, { childList: true, subtree: true });
        </script>
        """, unsafe_allow_html=True)
        
        prompt = st.chat_input("Type your message here...", key="stress_chat_input")
        if prompt:
            self._handle_user_message(messages_container, prompt)

    def _render_chat_history(self):
        """Render existing chat messages"""
        for message in st.session_state.stress_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant" and "message_id" in message:
                    message_links = st.session_state.message_links.get(message["message_id"], [])
                    self._render_message_links(message["message_id"], message_links)

def main():
    chat = StressReductionChat()
    chat.render_interface()

if __name__ == "__main__":
    main() 