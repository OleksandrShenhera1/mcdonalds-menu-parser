import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

# Avoiding python request
user = fake_useragent.UserAgent().random

header = {'User-Agent' : user}

# Link to menu website
link = "https://www.mcds-menu.com/"

response = requests.get(link, headers= header).text

soup = BeautifulSoup(response, 'lxml')

rows = soup.find_all('div', lambda x: x and 'wp-block-columns' in x)

with open('Mc_menu.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Price', 'Calories'])
    for row in rows:
        columns = row.find_all('div', class_=lambda x: x and 'wp-block-column' in x)
        for col in columns:
            # All tags (blocks)
            allTag = col.find_all('p', class_= 'has-text-align-center')
            
            # Name tag
            name = ''

            if len(allTag) > 0:
                aTag = allTag[0].find('a')
                if aTag:
                    name = aTag.text.strip()
                else:
                    name = allTag[0].text.strip()

            print(name)
            # Price tags & Calories tags
            price = ''
            calories = ''

            if len(allTag) > 1:
                price = allTag[1].text.strip()
                if '|' in price:
                    parts = price.replace('Price - ', '').split('|')
                    price = parts[0].strip() if len(parts) > 0 else ''
                    calories = parts[1].strip() if len(parts) > 1 else ''
                else:
                    price = price.replace('Price - ', '').strip()
            
            # Save to CSV
            if name or price or calories:
                writer.writerow([name, price, calories])


        
 
        