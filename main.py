"""
Document Q&A Bot - Main application file
"""
import os
import streamlit as st
import datetime
import warnings
from langchain_core.messages import HumanMessage, AIMessage

# Import from project modules
from document_utils import process_documents, generate_response
from ui_components import setup_chat_styling, get_chat_download_link

# Suppress warnings
warnings.filterwarnings("ignore")

os.environ["OPENAI_API_KEY"] = ""
os.environ["GOOGLE_API_KEY"] = ""

LLM_MODELS = ["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-4o-mini", "gpt-3.5-turbo", 
              "gemini-2.5-flash-preview-04-17", "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-pro"]

def initialize_session_state():
    """Initialize session state variables"""
    
    # Initialize chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize vector store
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    
    # Initialize message timestamps
    if "message_timestamps" not in st.session_state:
        st.session_state.message_timestamps = {}

def render_chat_messages(chat_placeholder):
    """Render all chat messages with styling"""
    
    messages_html = ""
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            messages_html += f'<div class="user-bubble">{message.content}</div>'
        else:
            messages_html += f'<div class="assistant-bubble">{message.content}</div>'
    
    # Display all messages at once
    chat_placeholder.markdown(messages_html, unsafe_allow_html=True)

def add_message(message, is_user=True):
    """Add a message to the chat history with timestamp"""
    
    st.session_state.messages.append(message)
    message_index = len(st.session_state.messages) - 1
    st.session_state.message_timestamps[message_index] = datetime.datetime.now().isoformat()

def handle_user_query(user_query, llm_model, chat_placeholder):
    """Process user query and update the chat interface"""
    
    if not st.session_state.vectorstore:
        # Add user message
        user_message = HumanMessage(content=user_query)
        add_message(user_message, is_user=True)
        render_chat_messages(chat_placeholder)
        
        # Add system response for missing documents
        response = "⚠️ Please process documents before asking questions."
        assistant_message = AIMessage(content=response)
        add_message(assistant_message, is_user=False)
        render_chat_messages(chat_placeholder)
        return

    # Add user message
    user_message = HumanMessage(content=user_query)
    add_message(user_message, is_user=True)
    render_chat_messages(chat_placeholder)
    
    # Create a separate container for the spinner
    spinner_container = st.container()
    
    with spinner_container:
        with st.spinner("🤖 Thinking..."):
            try:
                # Get chat history for context
                chat_history_text = get_formatted_chat_history()
                
                # Generate response
                answer = generate_response(user_query, llm_model, chat_history_text)
                
                # Add AI message to chat history
                assistant_message = AIMessage(content=answer)
                add_message(assistant_message, is_user=False)

            except Exception as e:
                # Handle error
                error_msg = f"🚫 Error generating response: {str(e)}"
                st.error(error_msg)
                
                # Prepare user-friendly error message
                if "AuthenticationError" in str(e):
                    error_response = "⚠️ Please check your OpenAI API key."
                else:
                    error_response = f"🚫 Sorry, I encountered an error: {str(e)}"
                
                # Add error message to chat history
                assistant_message = AIMessage(content=error_response)
                add_message(assistant_message, is_user=False)
            
            # Clear the spinner
            spinner_container.empty()
    
    # Final refresh of the chat display
    render_chat_messages(chat_placeholder)

def get_formatted_chat_history():
    """Format recent chat history for context"""
    
    chat_history_text = ""
    # Get all previous messages excluding the most recent
    recent_messages = st.session_state.messages if len(st.session_state.messages) > 1 else []
    
    for msg in recent_messages:
        if isinstance(msg, HumanMessage):
            chat_history_text += f"User: {msg.content}\n"
        else:
            chat_history_text += f"Assistant: {msg.content}\n"
    
    return chat_history_text

def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(page_title="Q&A RAG ChatBot", page_icon="🧠", layout="wide")
    st.title("🧠 Q&A RAG ChatBot")
    
    # Apply custom styling
    setup_chat_styling()
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for configuration and uploads
    with st.sidebar:
        st.header("🤖 Configuration")
        
        llm_model = st.selectbox(
            "Select LLM Model", 
            options=LLM_MODELS,
            index=None
            )
        
    if llm_model:
        with st.sidebar:

            api_key = st.text_input("Enter your API key for selected LLM", type="password")
            
            if "gemini" in llm_model:
                os.environ["GOOGLE_API_KEY"] = api_key
            else:
                os.environ["OPENAI_API_KEY"] = api_key
            
            st.header("Upload Documents")
            uploaded_files = st.file_uploader(
                "Upload your documents (.pdf, .docx, .txt)",
                type=["txt", "pdf", "docx"],
                accept_multiple_files=True,
            )

            process_button = st.button("Process Documents")

        # Process documents when button is clicked
        if process_button and uploaded_files:
            with st.spinner("Processing documents..."):
                process_documents(uploaded_files, llm_model)
        
        # Display chat interface if files have been uploaded
        if uploaded_files:
            # Inform the user that the input files are processed and passed to vectorstore
            if st.session_state.vectorstore:
                st.sidebar.success(f"✅ Successfully processed documents !")
                
            # Display chat history
            chat_container = st.container()
            with chat_container:
                chat_placeholder = st.empty()
                render_chat_messages(chat_placeholder)
                
            # Chat input
            user_query = st.chat_input("Ask a question about your documents...")
            
            if user_query:
                handle_user_query(user_query, llm_model, chat_placeholder)
                
            if st.session_state.messages:
                # Download chat history button
                st.sidebar.markdown(get_chat_download_link(), unsafe_allow_html=True)
        else:
            # Reset chat messages if new document uploaded
            st.session_state.messages = []
            st.session_state.vectorstore = None
    else:
        st.info("⚠️ Please select an LLM Model to proceed")

if __name__ == "__main__":
    main()