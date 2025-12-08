import os
import pdf2image
import pytesseract
from PIL import Image
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from image_to_text import text_extraction

from dotenv import load_dotenv

load_dotenv()

def process_pdf(pdf_file_path: str):

    reader = PdfReader(pdf_file_path)
    text_content = ""
    for page in reader.pages:
        text_content += page.extract_text() or ""

    if text_content.strip() == "":
        full_text = text_extraction(pdf_file_path,300)
        docs = [Document(page_content=full_text)]
    else:
        loader = PyPDFLoader(pdf_file_path)
        docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    reader = PdfReader(pdf_file_path)
    meta_data = reader.metadata

    db = FAISS.from_documents(chunks, embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True, output_key='answer'
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm, 
    retriever=retriever, 
    memory=memory, 
    return_source_documents=False
    )

    return qa_chain