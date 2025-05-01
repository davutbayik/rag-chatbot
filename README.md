# Document Q&A Bot

A Streamlit application that allows users to upload documents and ask questions about them using Retrieval-Augmented Generation (RAG).

## Features

- Upload and process multiple document types (PDF, DOCX, TXT)
- Ask questions about your document content
- WhatsApp-like chat interface
- Download conversation history

## Project Structure

The application is organized into three simple Python files:

1. `app.py` - Main application file with Streamlit UI and user interactions
2. `document_utils.py` - Document processing and RAG functionality
3. `ui_components.py` - UI styling and helper components

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Enter your OpenAI API key in the sidebar
2. Upload one or more documents (PDF, DOCX, or TXT format)
3. Click "Process Documents"
4. Ask questions about your documents in the chat interface
5. Download your chat history using the link in the sidebar

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for accessing OpenAI embeddings and completions APIs