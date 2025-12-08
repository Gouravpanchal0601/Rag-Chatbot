# 📘 RAG ChatBot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to
upload PDF documents and ask context-aware questions. It
extracts relevant information from the documents and generates accurate,
conversational, and grounded responses. The system combines document
retrieval with LLM reasoning, ensuring reliable answers backed by
the uploaded content.

------------------------------------------------------------------------

## 🚀 Features

-   📄 Upload PDF files (up to 200MB)
-   🔍 Intelligent text extraction & chunking
-   🤖 Context-aware question answering using RAG
-   ⚡ Fast, accurate retrieval from vector database
-   💬 Chat interface for smooth conversational experience
-   🧠 Reduces hallucinations by grounding answers in the document

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Python**
-   **Streamlit** -- UI
-   **LangChain / LlamaIndex** -- RAG pipeline
-   **FAISS / ChromaDB** -- Vector database
-   **OpenAI / HuggingFace Embeddings**

------------------------------------------------------------------------

## 📁 Project Structure

    📦 rag-chatbot
    ├── app.py               # Streamlit UI
    ├── rag_pipeline.py      # RAG logic (embeddings, retrieval, generation)
    ├── utils.py             # Helper functions
    ├── requirements.txt     # Dependencies
    ├── README.md            # Project documentation
    └── assets/              # Images, icons, etc.

------------------------------------------------------------------------

## 🧠 How It Works

1.  User uploads a PDF.
2.  Text is extracted and split into chunks.
3.  Chunks are converted into vector embeddings.
4.  Embedded vectors are stored in a vector database.
5.  User asks a question.
6.  System retrieves the most relevant chunks.
7.  LLM generates a grounded answer using retrieved context.

This ensures reliable, factual, and document-based responses.

------------------------------------------------------------------------

## ▶️ Getting Started

### 1️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 2️⃣ Run the Application

``` bash
streamlit run app.py
```

### 3️⃣ Open in Browser

    http://localhost:8501

------------------------------------------------------------------------

## 📤 How to Use

1.  Launch the app.
2.  Upload a PDF using the file uploader.
3.  Wait for processing.
4.  Start chatting and ask document-related questions.

------------------------------------------------------------------------

## 📸 Screenshots

*Add UI screenshots here.*

------------------------------------------------------------------------

## 🧩 Future Enhancements

-   Multi-PDF conversation support
-   Embedding caching for faster reloads
-   Chat export feature
-   Model selection option

------------------------------------------------------------------------

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull
requests.

------------------------------------------------------------------------

## 📜 License

This project is licensed under the **MIT License**.

------------------------------------------------------------------------
