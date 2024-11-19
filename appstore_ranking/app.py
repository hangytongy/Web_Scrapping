import requests
from bs4 import BeautifulSoup
import time

def main(url):
    
    # Headers to mimic a browser visit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    # Make the request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.content, "html.parser")
    
        # Extract the app name
        app_name = soup.find("h1", class_="product-header__title").get_text(strip=True) if soup.find("h1", class_="product-header__title") else "N/A"
    
        # Extract the developer name
        developer = soup.find("h2", class_="product-header__identity").get_text(strip=True) if soup.find("h2", class_="product-header__identity") else "N/A"
    
        # Extract the app rating
        rating_element = soup.find("a", class_="inline-list__item")
        rating = rating_element.get_text(strip=True) if rating_element else "No rating available"
    
        # Print the results
        print(f"App Name: {app_name}")
        print(f"Developer: {developer}")
        print(f"Rating: {rating}")

        text = f'\nApp Name : {app_name} \nRating: {rating}\n'
        return text
    
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

def post_message(message):

    tele_chatid = ''
    thread_id = ''
    api_key = ''
    url = f"https://api.telegram.org/bot{api_key}/sendMessage"

    payload = {'chat_id' : tele_chatid,'message_thread_id' : thread_id ,'text' : message, 'parse_mode' : "HTML"}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("post sucessful")
    else:
        print(f"error in posting {response}")


apps = { 'coinbase' : "https://apps.apple.com/us/app/coinbase-buy-bitcoin-ether/id886427730",
        'robinhood' : "https://apps.apple.com/us/app/robinhood-investing-for-all/id938003185",
        'phantom' : "https://apps.apple.com/us/app/phantom-crypto-wallet/id1598432977",
        'moonshot' : "https://apps.apple.com/us/app/moonshot/id6503993131",
        'metamask' : "https://apps.apple.com/us/app/metamask-blockchain-wallet/id1438144202" 
       }

full_text = "---APP RANKINGS---\n"

for app in apps:
    url = apps[app]
    text = main(url)
    full_text = full_text + text
    time.sleep(5)

post_message(full_text)