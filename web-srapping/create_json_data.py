import pandas as pd
import json

# Read restaurant info
restaurants_info = pd.read_csv('restaurants_info.csv')

# Function to map dietary labels
def map_dietary(label):
    label = label.strip().lower()
    return ["veg"] if label == "veg" else ["non-veg"]

def map_features(label):
    print(label)
    label = label.strip().lower()
    print(label)
    return ['Best Seller'] if label == "['best seller']" else []

restaurants = []

for idx, row in restaurants_info.iterrows():
    restaurant_id = idx + 1
    # Prepare operating hours (using same value for mon-fri and sat-sun)
    operating_hours = {
        "mon-fri": row['opening_hours'],
        "sat-sun": row['opening_hours']
    }
    contact = {
        "phone": f"+{row['phone_number']}"
    }
    
    # Read corresponding menu CSV
    menu_df = pd.read_csv(f"{row['menu_csv']}")
    menu = []
    for i, item in menu_df.iterrows():
        item_id = restaurant_id * 100 + (i + 1)
        menu.append({
            "id": item_id,
            "name": item['item_name'],
            "description": item['description'],
            "price": int(item['price']),
            "dietary": map_dietary(item['dietery']),
            "features":map_features(item['features']),
            "rating":item['rating'],
            "available": True
        })
    
    # Build restaurant entry
    restaurants.append({
        "id": restaurant_id,
        "name": row['restaurant_name'],
        "location": row['restaurant_location'],
        "rating": float(row['rating']),
        "operating_hours": operating_hours,
        "contact": contact,
        "menu": menu
    })

output_path = 'restaurants.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, indent=2, ensure_ascii=False)

print(f"JSON file created at: {output_path}")