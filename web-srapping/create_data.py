from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import re
from dotenv import load_dotenv
import os

load_dotenv()

def clean_filename(name):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name.strip()) if name else "unknown_restaurant"

def clean_opening_hours(hours):
    if hours:
        return re.sub(r'\s*\(.today.\)', '', hours, flags=re.IGNORECASE).strip()
    return ""

def scrape_info(url, phone_class, hours_class, name_class, address_class, rating_class):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    # Restaurant name
    restaurant_name = ""
    if name_class:
        name_elements = driver.find_elements(By.CLASS_NAME, name_class)
        for el in name_elements:
            if el.text.strip():
                restaurant_name = el.text.strip()
                break
    # Restaurant location
    restaurant_location = ""
    if address_class:
        address_elements = driver.find_elements(By.CLASS_NAME, address_class)
        for el in address_elements:
            if el.text.strip():
                restaurant_location = el.text.strip()
                break
    # Phone number
    phone_number = ""
    if phone_class:
        phone_number_class = driver.find_elements(By.CLASS_NAME, phone_class)
        for el in phone_number_class:
            if el.text.strip():
                phone_number = el.text.strip()
                break
    # Opening hours
    opening_hours = ""
    if hours_class:
        opening_hours_class = driver.find_elements(By.CLASS_NAME, hours_class)
        for el in opening_hours_class:
            if el.text.strip():
                opening_hours = clean_opening_hours(el.text.strip())
                break
    # Rating
    rating = ""
    if rating_class:
        rating_class = driver.find_elements(By.CLASS_NAME, rating_class)
        for el in rating_class:
            if el.text.strip():
                rating = el.text.strip()
                break
    driver.quit()
    return {
        "restaurant_name": restaurant_name,
        "restaurant_location": restaurant_location,
        "phone_number": phone_number,
        "opening_hours": opening_hours,
        "rating":rating
    }

def scrape_menu(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    names = driver.find_elements(By.CLASS_NAME, "dwSeRx")
    prices = driver.find_elements(By.CLASS_NAME, "chixpw")
    descriptions = driver.find_elements(By.CLASS_NAME, "gCijQr")
    svg=driver.find_elements(By.CLASS_NAME,"sc-jxOSlx")
    rating=driver.find_elements(By.CLASS_NAME,"knBukL")
    menu_items = []
    for i in range(min(len(names), len(prices), len(descriptions), len(svg),len(rating))):
        feature=[]
        dietery="Veg"
        s=svg[i].find_element(By.TAG_NAME,"use").get_attribute("xlink:href")
        print(s)
        s=s[:-2]
        if s=="/food/sprite-CiiAtHUR.svg#bestseller": feature.append("Best Seller")
        s=s[-6:]
        if s=="NonVeg": dietery="Non Veg"
        menu_items.append({
            "item_name": names[i].text,
            "price": prices[i].text,
            "description": descriptions[i].text,
            "dietery":dietery,
            "features":feature,
            "rating":rating[i].text
        })
    driver.quit()
    return menu_items

if __name__ == "__main__":
    restaurant_pairs = [
        (
            "https://www.zomato.com/lucknow/mashi-biryani-world-gomti-nagar",
            "https://www.swiggy.com/city/lucknow/mashi-biryani-world-gomti-nagar-rest94712",
            "leEVAg", "dfwCXs", "fwzNdh", "ckqoPM","cILgox"
        ),
        (
            "https://www.zomato.com/lucknow/manish-eating-point-gomti-nagar", 
            "https://www.swiggy.com/city/lucknow/the-manish-eating-point-viram-khand-gomti-nagar-rest59253", 
            "leEVAg", "dfwCXs", "fwzNdh", "ckqoPM","cILgox"
        ),
        (
            "https://www.zomato.com/lucknow/kuduk-chicken-1-gomti-nagar",
            "https://www.swiggy.com/city/lucknow/kuduk-chicken-gomti-nagar-rest211940",
            "leEVAg", "dfwCXs", "fwzNdh", "ckqoPM","cILgox"
        ),
        (
            "https://www.zomato.com/lucknow/moti-mahal-delux-2-gomti-nagar",
            "https://www.swiggy.com/city/lucknow/moti-mahal-delux-gomti-nagar-rest429875",
            "leEVAg", "dfwCXs", "fwzNdh", "ckqoPM","cILgox"
        ),
        (
            "https://www.zomato.com/lucknow/aryan-familys-delight-4-gomti-nagar",
            "https://www.swiggy.com/city/lucknow/aryan-familys-delight-shaheed-path-sushant-golf-city-rest105935",
            "leEVAg", "dfwCXs", "fwzNdh", "ckqoPM","cILgox"
        ),
        (
            "https://www.zomato.com/lucknow/burger-king-3-gomti-nagar",
            "https://www.swiggy.com/city/lucknow/burger-king-phoenix-plassio-mall-arjunganj-rest318544",
            "leEVAg", "dfwCXs", "fwzNdh", "ckqoPM","cILgox"
        ),
        (
            "https://www.zomato.com/lucknow/dosa-planet-gomti-nagar",
            "https://www.swiggy.com/city/lucknow/dosa-planet-pheonix-palassio-mall-gomti-nagar-rest402624",
            "leEVAg", "dfwCXs", "fwzNdh", "ckqoPM","cILgox"
        )
    ]

    restaurant_info_list = []
    for idx, (zomato_url, swiggy_url, phone_class, hours_class, name_class, address_class, rating_class) in enumerate(restaurant_pairs):
        info = scrape_info(zomato_url, phone_class, hours_class, name_class, address_class,rating_class)
        menu = scrape_menu(swiggy_url)
        menu_csv_filename = clean_filename(info["restaurant_name"]) + ".csv" if info["restaurant_name"] else f"restaurant{idx+1}.csv"
        with open(menu_csv_filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["item_name", "price", "description","dietery","features","rating"])
            writer.writeheader()
            writer.writerows(menu)
        restaurant_info_list.append({
            "restaurant_name": info["restaurant_name"],
            "restaurant_location": info["restaurant_location"],
            "phone_number": info["phone_number"],
            "opening_hours": info["opening_hours"],
            "rating":info["rating"],
            "menu_csv": menu_csv_filename,
        })

    with open("restaurants_info.csv", mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["restaurant_name", "restaurant_location", "phone_number", "opening_hours", "rating", "menu_csv"])
        writer.writeheader()
        writer.writerows(restaurant_info_list)

    print(f"Saved {len(restaurant_info_list)} restaurants to restaurants_info.csv")