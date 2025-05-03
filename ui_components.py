"""
UI components and styling for Document Q&A Bot
"""
import streamlit as st
import json
import base64
import datetime
from langchain_core.messages import HumanMessage


def setup_chat_styling():
    """Apply custom CSS styling for the chat interface"""
    st.markdown("""
    <style>
        /* Hide upper menu */
        Main Menu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}           

        /* Message container styling */
        .user-bubble {
            background-color: #DCF8C6;
            color: black;
            padding: 12px;
            border-radius: 15px 15px 0 15px;
            margin: 10px 10px 10px auto;
            max-width: 80%;
            display: inline-block;
            float: right;
            clear: both;
        }
        .assistant-bubble {
            background-color: #F2F2F2;
            color: black;
            padding: 12px;
            border-radius: 15px 15px 15px 0;
            margin: 10px auto 10px 10px;
            max-width: 80%;
            display: inline-block;
            float: left;
            clear: both;
        }
        
        /* Hide the default Streamlit chat message styling */
        .stChatMessage {
            background-color: transparent !important;
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)


def get_chat_download_link():
    """
    Generate a download link for the chat history.
    
    Returns:
        str: HTML link for downloading chat history as JSON
    """
    
    # Convert messages to a simpler format for download
    chat_history = []
    
    for i, message in enumerate(st.session_state.messages):
        # Get timestamp for this message
        if i not in st.session_state.message_timestamps:
            # If no timestamp exists, use current time
            st.session_state.message_timestamps[i] = datetime.datetime.now().isoformat()
            
        if isinstance(message, HumanMessage):
            chat_history.append({
                "role": "user", 
                "content": message.content,
                "timestamp": st.session_state.message_timestamps[i]
            })
        else:
            chat_history.append({
                "role": "assistant", 
                "content": message.content,
                "timestamp": st.session_state.message_timestamps[i]
            })

    # Create JSON string with ensure_ascii=False for proper Unicode support
    json_str = json.dumps(chat_history, indent=3, ensure_ascii=False)
    
    # Create download link with UTF-8 encoding
    b64 = base64.b64encode(json_str.encode('utf-8')).decode()
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_{date_str}.json"
    href = f'<a href="data:file/json;charset=utf-8;base64,{b64}" download="{filename}">Download Chat History</a>'
    
    return href
