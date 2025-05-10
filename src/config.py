import os
from pinecone import Pinecone
from groq import Groq
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# HUGGING_FACE_MODEL = os.getenv("HUGGING_FACE_MODEL")
# LLAMA_MODEL = os.getenv("LLAMA_MODEL")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_INDEX = os.getenv("PINECONE_INDEX")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

HUGGING_FACE_MODEL = st.secrets["api_keys"]["HUGGING_FACE_MODEL"]
LLAMA_MODEL = st.secrets["api_keys"]["LLAMA_MODEL"]
PINECONE_API_KEY = st.secrets["api_keys"]["PINECONE_API_KEY"]
PINECONE_INDEX = st.secrets["api_keys"]["PINECONE_INDEX"]
GROQ_API_KEY = st.secrets["api_keys"]["GROQ_API_KEY"]


pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
index = pinecone_client.Index(PINECONE_INDEX)
client = Groq(api_key=GROQ_API_KEY)