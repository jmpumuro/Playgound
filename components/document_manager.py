import streamlit as st
import os
from rag import get_rag_system
import shutil
from typing import List
from pathlib import Path
import mimetypes

class DocumentManager:
    def __init__(self):
        self.documents_dir = "documents"
        self._ensure_documents_directory()
        self._init_file_icons()

    def _init_file_icons(self):
        """Initialize file type icons"""
        self.file_icons = {
            '.txt': '📄',
            '.pdf': '📕',
            '.md': '📝',
            '.docx': '📘',
            'folder': '📁'
        }

    def _ensure_documents_directory(self):
        """Ensure the documents directory exists"""
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)

    def _get_file_icon(self, filename: str) -> str:
        """Get the appropriate icon for a file type"""
        _, ext = os.path.splitext(filename)
        return self.file_icons.get(ext.lower(), '📄')

    def _get_file_size(self, filepath: str) -> str:
        """Get human-readable file size"""
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} GB"

    def _get_existing_documents(self) -> List[dict]:
        """Get list of existing documents with metadata"""
        if not os.path.exists(self.documents_dir):
            return []
        
        documents = []
        for f in os.listdir(self.documents_dir):
            filepath = os.path.join(self.documents_dir, f)
            if os.path.isfile(filepath) and f.endswith(('.txt', '.pdf', '.md', '.docx')):
                documents.append({
                    'name': f,
                    'size': self._get_file_size(filepath),
                    'icon': self._get_file_icon(f),
                    'modified': os.path.getmtime(filepath)
                })
        return sorted(documents, key=lambda x: x['name'])

    def render_interface(self):
        """Render the document management interface"""

        
        # File upload section with styled drop zone
        st.markdown("""
        <div class="upload-zone">
            <h4>📥 Upload Documents</h4>
            <p style="color: #888;">Drag and drop files here • Limit 200MB per file</p>
            <p style="color: #666; font-size: 0.8em;">Supported formats: TXT, PDF, MD, DOCX</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Upload Documents",
            accept_multiple_files=True,
            type=['txt', 'pdf', 'md', 'docx'],
            label_visibility="collapsed"
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = os.path.join(self.documents_dir, uploaded_file.name)
                
                if os.path.exists(file_path):
                    st.warning(f"File {uploaded_file.name} already exists. Skipping...")
                    continue
                
                with open(file_path, "wb") as f:
                    shutil.copyfileobj(uploaded_file, f)
                st.success(f"Successfully uploaded {uploaded_file.name}")

        # Display existing documents in file system style
        existing_docs = self._get_existing_documents()
        if existing_docs:
            st.markdown("#### Knowledge Base Files")
            st.markdown('<div class="file-system">', unsafe_allow_html=True)
            
            for doc in existing_docs:
                col1, col2, col3 = st.columns([6, 2, 1])
                with col1:
                    st.markdown(
                        f'<div class="file-row">'
                        f'<span class="file-icon">{doc["icon"]}</span>'
                        f'<span class="file-name">{doc["name"]}</span>'
                        f'<span class="file-size">{doc["size"]}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                with col3:
                    if st.button("🗑️", key=f"delete_{doc['name']}", help="Delete file", use_container_width=True):
                        try:
                            os.remove(os.path.join(self.documents_dir, doc['name']))
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting {doc['name']}: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Index management with styled button
        st.markdown("""
        <div style="margin-top: 30px;">
            <h4> Index Management</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                '<p style="color: #888;">Update the AI\'s knowledge base with the current documents</p>',
                unsafe_allow_html=True
            )
        with col2:
            if st.button("Update Index", type="primary", use_container_width=True):
                with st.spinner("Updating knowledge base..."):
                    try:
                        rag_system = get_rag_system()
                        rag_system.load_documents()
                        st.success("✅ Knowledge base updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error updating index: {str(e)}")

def render_document_manager():
    """Render the document manager interface"""
    manager = DocumentManager()
    manager.render_interface() 