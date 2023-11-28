import discord
import asyncio
from bs4 import BeautifulSoup
import requests
import json

client = discord.Client()
# File to store the data
filename = 'previous_items.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # Add other headers or cookies as needed
}

# Function to load previously scraped items
def load_previous_items():
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

def save_items(items):
    filename = 'previous_items.json'  # The path to your JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(items, file, indent=4, ensure_ascii=False)


# Function to scrape the website
async def scrape_website():
    url = 'https://biletinial.com/tr-tr/spor'
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
        
        return result
    else:
        print(f"Failed to retrieve content: {response.status_code}")

# Function to check for updates and send messages
async def check_for_updates():
    await client.wait_until_ready()
    channel = client.get_channel(0000)  # Replace with your channel ID
    previous_items = load_previous_items()



    while not client.is_closed():
        current_items = await scrape_website()
        new_items = [item for item in current_items if item not in previous_items]

        if new_items:
            for item in new_items:
                message = f'**Lig {item["lig"]}**: {item["text"]} \n{item["img_url"]}'
                await channel.send(message)
                

        save_items(current_items)
        await asyncio.sleep(1800)  # Run every 1/2 hour

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    greeting_channel = client.get_channel(0000)  # Replace with your channel ID
    await greeting_channel.send('Hello! I am up and running!')

# Run the bot
client.loop.create_task(check_for_updates())
client.run('#####')  # Replace with your bot token