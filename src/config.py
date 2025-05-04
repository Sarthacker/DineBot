import os
from pinecone import Pinecone
from groq import Groq
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# HUGGING_FACE_MODEL = st.secrets["HUGGING_FACE_MODEL"]
# LLAMA_MODEL = st.secrets["LLAMA_MODEL"]
# PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
# PINECONE_INDEX = st.secrets["PINECONE_INDEX"]
# GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

HUGGING_FACE_MODEL = os.getenv("HUGGING_FACE_MODEL")
LLAMA_MODEL = os.getenv("LLAMA_MODEL")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
index = pinecone_client.Index(PINECONE_INDEX)
client = Groq(api_key=GROQ_API_KEY)