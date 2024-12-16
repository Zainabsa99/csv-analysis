import streamlit as st
from langchain.document_loaders import CSVLoader
from langchain.chains import ConversationalRetrievalChain
from store_index import *
from llm_loader import load_llm
import tempfile
from streamlit_chat import message
from langchain.llms import CTransformers
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain_community.llms import Replicate
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler, BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.llms import Replicate
from langchain_community import llms
import streamlit as st
import tempfile
import pandas as pd
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from streamlit_chat import message

# Load your pre-trained LLaMA2 model
llm = load_llm()

st.title("Analyze Log Files for IOCs with LLaMA3 🦙")
st.sidebar.header("Upload Your Log File")

# Upload CSV file
uploaded_file = st.sidebar.file_uploader("Upload CSV Log File", type="csv")

if uploaded_file:
    try:
        # Save the file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Load the CSV file
        st.write("### Processing Uploaded Log File...")
        csv_loader = CSVLoader(file_path=temp_file_path, encoding='UTF-8', csv_args={'delimiter': ','})
        data = csv_loader.load()

        # Show the first few rows for verification
        st.write("#### Preview of Uploaded Log File")
        st.write(data[:5])  # Display first 5 rows

        # Create FAISS Vector Database
        st.write("### Setting Up Vector Store...")
        db = store_index(data=data)

        # Create Conversational Retrieval Chain
        st.write("### Setting Up LLaMA2 Analysis Chain...")
        llm = load_llm()
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={"k": 3}),
        )

        # Query for IOC analysis
        query = """Analyze the log file. Identify if it contains any Indicators of Compromise (IOCs) and specify their types. 
                   If no IOCs are present, confirm the log is clean."""
        st.write("### Analyzing Log File...")
        llm_response = chain.invoke({"question": query, "chat_history": {}})
        
        # Display the response
        st.write("### LLaMA2 Analysis Result")
        st.text(llm_response["answer"])

    except Exception as e:
        st.error(f"An error occurred: {e}")