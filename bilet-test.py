import requests
from bs4 import BeautifulSoup
import json

url = 'https://biletinial.com/tr-tr/spor'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # Add other headers or cookies as needed
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    targeted_ligs = {'117', '156', '157'}
    items = soup.find_all('li', {'data-lig': lambda x: x in targeted_ligs})
    
    result = []
    for item in items:
        lig = item['data-lig']
        text = item.text.strip().replace('\n', ' ').replace('\r', ' ')
        img_tag = item.find('img')
        img_url = img_tag['src'] if img_tag else 'No image found'
        result.append({'lig': lig, 'text': text, 'img_url': img_url})

    pretty_json = json.dumps(result, indent=4, ensure_ascii=False)   
    print(pretty_json)
else:
    print(f"Failed to retrieve content: {response.status_code}")