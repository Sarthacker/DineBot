import streamlit as st
from src.utils import handle_scope_check, ask_bot

st.set_page_config(page_title="Zomato Chat Bot", layout="wide")

SYSTEM_INITIAL = """You are a helpful and friendly zomato assistant that answers user queries related to food and restaurants./
                You are provided with a user query and a context that includes the restaurant name, the dish name,
                its price, and a description of the dish. Based on this context, provide accurate, concise,
                and conversational responses to the user's questions./
                If the query is unrelated to the provided context,
                politely guide the user back to asking about food or restaurants./
                If the user strays, gently guide them back to food/restaurants."""
if "llm_messages" not in st.session_state:
    st.session_state.llm_messages = []

st.title("Food & Restaurant Chatbot")

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")


if submitted and user_input:
    if handle_scope_check(user_input):
        # Ask bot and update history
        reply = ask_bot(st.session_state.llm_messages, user_input)

# Display chat
for msg in st.session_state.llm_messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"]=="assistant":
        st.chat_message("assistant").write(msg["content"])