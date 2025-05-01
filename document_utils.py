"""
Document processing and RAG functionality for Document Q&A Bot
"""
import os
import tempfile
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TEMPERATURE = 0
TOP_K_DOCUMENTS = 5

def process_documents(files):
    """
    Process uploaded documents and create a vector store.
    
    Args:
        files: List of uploaded file objects
    """
    documents = []
    temp_files = []
    
    try:
        # Process each uploaded file
        for file in files:
            try:
                # Save the uploaded file to a temporary location
                temp_path = save_uploaded_file(file)
                temp_files.append(temp_path)
                
                # Load documents based on file type
                loader = get_document_loader(temp_path, file.name)
                documents.extend(loader.load())
                
            except Exception as e:
                st.error(f"🚫 Error processing {file.name}: {str(e)}")
                continue
        
        if not documents:
            st.error("🚫 No documents were successfully processed.")
            return
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        try:
            embeddings = OpenAIEmbeddings()
            st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
        except Exception as e:
            st.sidebar.error(f"🚫 Error creating embeddings: {str(e)}")
            if "AuthenticationError" in str(e):
                st.sidebar.warning("⚠️ Please check your OpenAI API key.")
                
    finally:
        # Clean up temporary files
        for temp_path in temp_files:
            try:
                os.unlink(temp_path)
            except:
                pass  # Silent fail if cleanup fails

def save_uploaded_file(uploaded_file):
    """
    Save an uploaded file to a temporary location.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Path to the temporary file
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name
    
    return temp_path

def get_document_loader(file_path, file_name):
    """
    Get the appropriate document loader based on file extension.
    
    Args:
        file_path: Path to the file
        file_name: Name of the file
        
    Returns:
        loader: LangChain document loader
    """
    file_extension = os.path.splitext(file_name)[1].lower()
    
    if file_extension == ".pdf":
        return PyPDFLoader(file_path)
    elif file_extension == ".docx":
        return Docx2txtLoader(file_path)
    elif file_extension == ".txt":
        return TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def generate_response(user_query, llm_model, chat_history_text):
    """
    Generate a response using RAG.
    
    Args:
        user_query: User's question
        chat_history_text: Formatted chat history
        
    Returns:
        str: Generated answer
    """
    # Set up LLM
    if "gemini" in llm_model:
        llm = ChatGoogleGenerativeAI(temperature=TEMPERATURE, model=llm_model)
    else:
        llm = ChatOpenAI(temperature=TEMPERATURE, model=llm_model)
    
    # Get relevant documents
    retriever = st.session_state.vectorstore.as_retriever(
        search_kwargs={"k": TOP_K_DOCUMENTS}
    )
    relevant_docs = retriever.invoke(user_query)
    
    # Check if there are relevant documents
    if not relevant_docs:
        return ("I don't see any information in the uploaded documents that's relevant to your question. "
                "Please ask something related to the content of your documents, or upload additional materials if needed.")
    
    # Set up prompt template
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context:
    {context}
    
    Previous conversation:
    {chat_history}
    
    Question: {input}
    
    If the answer cannot be found in the provided context, respond with:
    "I don't have enough information in the uploaded documents to answer that question. Please ask something related to the content of your documents."
    
    Otherwise, provide a helpful and informative answer based solely on the context provided.
    """)
    
    # Create document chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    # Create retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    # Generate response
    response = retrieval_chain.invoke({
        "input": user_query,
        "chat_history": chat_history_text
    })

    return response["answer"]