import os
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PDF Chat with Gemini")
st.title("📄 Chat with PDF using Gemini + FAISS")

pdf_path = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_path is not None:
    with open("temp.pdf", "wb") as f:
        f.write(pdf_path.read())

    st.success("✅ PDF uploaded. Generating embeddings...")

    loader = PyPDFLoader("temp.pdf")
    documents = loader.load()

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))
    db = FAISS.from_documents(documents, embeddings)

    retriever = db.as_retriever()
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    st.info("Ready! Ask a question about your PDF:")

    query = st.text_input("❓ Your question:")
    if query:
        response = chain.run(query)
        st.write("💬", response)
