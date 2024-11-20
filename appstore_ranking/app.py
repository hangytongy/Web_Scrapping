import requests
from datetime import datetime
import time

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

def get_data(app_id,categories,date_current):
    
# Base URL
    url = 'https://app.sensortower.com/api/ios/category/category_history'

    # Query parameters
    params = {
        'app_ids[]': app_id,  # App ID
        'categories[]': categories,  # App Store categories
        'chart_type_ids[]': ['topfreeapplications'],
        'countries[]': 'US',  # Country code
        'end_date': date_current,  # End date
        'start_date': date_current,  # Start date
    }

    # Headers (if any authorization or specific headers are needed)
    headers = {
        'User-Agent': 'Your User Agent',  # Replace with your user agent string
        # 'Authorization': 'Bearer <token>',  # Uncomment if authentication is needed
    }

    # Sending the GET request
    response = requests.get(url, params=params, headers=headers)

    # Handling the response
    if response.status_code == 200:        
        app_dict = {}
        data = response.json()[app_id]['US']
        
        for category in categories:
            
            if category in data:
            
                category_name = data[category]['topfreeapplications']['category_name']
                rank = data[category]['topfreeapplications']['todays_rank']
                app_dict[category_name] = rank
            else:
                if category == '0':
                    app_dict['Overall'] = 'NA'
                    
        print(app_dict)
        return app_dict
    else:
        print(f"Failed! Status code: {response.status_code}, Response: {response.text}")

apps = { 'coinbase' : {'app_id' : '886427730', 'categories' : ['6015', '0']},
        'robinhood' : {'app_id' : '938003185', 'categories' : ['6015', '0']} ,
        'phantom' : {'app_id' : '1598432977', 'categories' : ['6002', '0']} ,
        'moonshot' : {'app_id' : '6503993131', 'categories' : ['6015', '0']} ,
        'metamask' : {'app_id' : '1438144202' , 'categories' : ['6002', '0']} 
       }

date_current = datetime.now().strftime('%Y-%m-%d')

app_all = {}

for app in apps:
    print(app)
    name = app
    app_id = apps[app]['app_id']
    categories = apps[app]['categories']
    app_all[name] = get_data(app_id,categories,date_current)
    time.sleep(15)

formatted_text = []
for app, rankings in app_all.items():
    ranking_info = ", ".join([f"{category}: {rank}" for category, rank in rankings.items()])
    formatted_text.append(f"\n{app.capitalize()}: \n{ranking_info}")

# Join and print the formatted text
output = "\n".join(formatted_text)
output = "---APP STORE RANKING---\n"+output

post_message(output)