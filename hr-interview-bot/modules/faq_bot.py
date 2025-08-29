import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq

def load_faq_bot():
    # Always resolve absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    faq_path = os.path.join(base_dir, "..", "data", "hr_faq.txt")

    if not os.path.exists(faq_path):
        st.error(f"⚠️ Missing file: {faq_path}")
        return None

    # Load HR FAQ text file
    loader = TextLoader(faq_path, encoding="utf-8")
    docs = loader.load()

    # Split into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create FAISS in memory
    db = FAISS.from_documents(chunks, embeddings)

    retriever = db.as_retriever()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile")

    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False  # can make True if you want sources
    )
    return qa

qa_chain = None

def faq_chatbot():
    global qa_chain
    if qa_chain is None:
        qa_chain = load_faq_bot()
        if qa_chain is None:
            return

    user_q = st.text_input("Ask me an HR question:")
    if st.button("Submit") and user_q:
        with st.spinner("Thinking..."):
            result = qa_chain({"question": user_q})

            # Some versions return "answer", others "result"
            answer = result.get("answer") or result.get("result")
            st.write("**Answer:**", answer)
