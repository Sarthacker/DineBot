import json
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

model=SentenceTransformer(os.getenv("HUGGING_FACE_MODEL"))
pc=Pinecone(api_key=os.getenv("PINECONE_API_KEY")).Index(os.getenv("PINECONE_INDEX"))

def getembeddings(texts):
    if isinstance(texts, str):
        texts = [texts]
    embeddings = model.encode(  
        texts,
        show_progress_bar=False,
        convert_to_numpy=True,
    )
    return embeddings.tolist()

def generate_chunks(restaurants):
    for r in restaurants:
        restId = r.get('id', 'none')
        name   = r.get('name', 'Unknown')
        location=r.get('location','Unknown')
        contact=r.get('contact',{})
        phone   =contact.get('phone','N/A')
        hours=r.get('operating_hours',{})
        print(hours)
        weekday_hours=hours.get('mon-fri','N/A')
        weekend_hours=hours.get('sat-sun','N/A')
        
        
        # text=f"{name} is a restaurant present at {location} which can be contacted at {phone}"
        chunks = []

        for item in r.get('menu', []):
            dish = item.get('name', 'Unnamed dish')
            desc = item.get('description', '').strip()
            features=item.get('features',[])
            if not desc:
                continue

            
            text= f"{dish} is served at {name} having description as follows: {desc}"
            chunks.append(text)

            embeddings = getembeddings(chunks)

            dish_embedding = embeddings[-1]

            data = {
                "id":      str(item.get('id', 'none')),
                "values":  dish_embedding,
                "metadata":{
                    "restaurant_id":   restId,
                    "restaurant_name": name,
                    "dish_name":       dish,
                    "description":     desc,
                    "price":           item.get('price', 'N/A'),
                    "dietary":         ", ".join(item.get('dietary', [])),
                    "operating_hours": f"Weekdays - {weekday_hours} Weekends - {weekend_hours}",
                    "features":        features,
                    "contact":         phone,
                    "available":       "yes" if item.get('available') else "no"
                }
            }

            pc.upsert([data])

    return chunks


if __name__ == "__main__":
    with open("restaurants.json", "r", encoding="utf-8") as f:
        restaurant_data = json.load(f)

    #Generate and print
    for sentence in generate_chunks(restaurant_data):
        print("-", sentence)