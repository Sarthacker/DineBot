import json 
from .config import index, client, LLAMA_MODEL,HUGGING_FACE_MODEL
from sentence_transformers import SentenceTransformer
from streamlit import write

model = SentenceTransformer(HUGGING_FACE_MODEL)

def handle_scope_check(user_query: str) -> bool:
    system_prompt = '''
        Task:
            You are a helpful and friendly chatbot that only answers queries related to dishes, food, restaurants, cuisines.
            If the user talks to you about any other topic refrain from answering and ask them to stick to the topics of "foods, retraurants or cuisines",
            except if user greets then normally greet him back (greetings include normal "hi,hello,good morning" .etc and closing greetings such as "thank you, good evening" .etc.).
            You need to give me only json response which contains two keys -
            first: result (0 if the user's query is not related to foods, dishes and restaurants/greeting queries and 1 if the query is related to that)
            second: your response
            
            For Example:
            "user_query":"what is the food prices of ABC dish at XYX restaurant?"
            output:{
                "result":"1"
                "response":your_response
            }
    '''
    response_str = client.chat.completions.create(
        model=LLAMA_MODEL,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_query}
        ]
    ).choices[0].message.content
    data = json.loads(response_str[response_str.find('{'):response_str.rfind('}')+1])
    if data.get("result") == "1":
        return True
    write(data.get("response", "Sorry, I can't help with that."))
    return False

def get_embeddings(texts):
    if isinstance(texts, str):
        texts = [texts]
    embeddings = model.encode(texts,
                            convert_to_numpy=True,
                            show_progress_bar=False)
    return embeddings[0].tolist()

def pinecone_search(query: str, top_k: int = 8):
    vec = get_embeddings(query)
    return index.query(vector=[vec], top_k=top_k, include_metadata=True)

def ask_bot(messages: list, user_query: str) -> str:
    # if there's no system message in messages yet, add it
    context = pinecone_search(user_query)
    if not any(m["role"] == "system" for m in messages):
        messages.append({
            "role": "system",
            "content": f'''
                Task:
                    You are a helpful and friendly zomato assistant that answers user queries related to food and restaurants.
                    You are provided with a user query and a context that includes the restaurant name, the dish name,
                    its price, and a description of the dish. Based on this context, provide accurate, concise,
                    and conversational responses to the user's questions.
                    If the query is unrelated to the provided context,
                    politely guide the user back to asking about food or restaurants.
                    If the user strays, gently guide them back to food/restaurants.
            '''
        })

    messages.append({
        "role": "system",
        "content": f"{context}"
    })
    messages.append({
        "role": "user",
        "content": user_query
    })

    chat_completion = client.chat.completions.create(
        model=LLAMA_MODEL,
        messages=messages
    )
    assistant_reply = chat_completion.choices[0].message.content
    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })
    # print(messages)
    return assistant_reply