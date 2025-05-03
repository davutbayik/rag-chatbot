# 📄🔍 RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot with a custom Streamlit interface that allows users to upload documents and ask questions about their content.

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b.svg)
![LangChain](https://img.shields.io/badge/LangChain-enabled-yellow)
![OpenAI](https://img.shields.io/badge/OpenAI-powered-000000.svg?logo=openai)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features
- 🤖 **LLM Model Selection**: Select desired LLM model from OpenAI or Gemini. 
- 📁 **Multi-Format Document Upload**: Supports PDF, DOCX, and TXT files.
- 💬 **Interactive Q&A**: Ask questions about your uploaded documents.
- 🎨 **Custom Chat Interface**: WhatsApp-like chat UI for a familiar user experience.
- 💾 **Conversation History**: Download your chat history for future reference.

## 🖥️ Live App

👉 Coming Soon

## 🧩 Tech Stack

- [Python 3.12](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://platform.openai.com/)
- [Gemini](https://aistudio.google.com)

## 🚀 Usage

1. **Select an LLM Model**: Select an LLM model for the chatbot from the given list. List consist of OpenAI and Gemini models.
2. **Upload Documents**: Use the sidebar to upload one or more documents (PDF, DOCX, or TXT).
3. **Ask Questions**: Type your questions in the chat input box. The chatbot will provide answers based on the content of your uploaded documents.
4. **Download History**: Click the "Download" button to save your conversation history.

## 🎥 Example Demo




## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/davutbayik/rag-chatbot.git
   cd rag-chatbot
   ```

2. **Create and activate a virtual environment (Optional-Recommended)**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:

   ```bash
   streamlit run main.py
   ```

## 🔑 Environment Variables

Create a `.env` file in the root directory with:

```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
```

## 📂 Project Structure

```
├── main.py               # Main Streamlit application
├── document_utils.py    # Document processing and RAG functionality
├── ui_components.py     # UI styling and helper components
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
└── README.md            # Project documentation
```

## 📄 License

This project is licensed under the terms of the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software as long as you include the original license.

## 📬 Contact

Made with ❤️ by [Davut Bayık](https://github.com/davutbayik) — feel free to reach out via GitHub for questions, feedback, or collaboration ideas.

---

⭐ If you found this project helpful, consider giving it a star!

*Happy chatting!* 💬📚
