import asyncio

import aiosqlite
import requests

from config import DB_URL
import db.database
from bs4 import BeautifulSoup

# стартовое сообщение
def print_banner(script_name, description=""):
    print("\n" + "="*50)
    print(f"{script_name}")
    print("="*50)
    if description:
        print(f"{description}")
    print("Скрипт успешно запущен!")
    print("="*50 + "\n")


print_banner(
    "Eros tracker",
    "Telegram nft gifts tracker"
)

res = requests.get('https://fragment.com/gifts')
html_content = res.text
links_data = []


class GiftCharacteristics:
    def __init__(self, collection_name, model):
        self.collection_name = collection_name
        self.model = model


def find_gift_by_name():
    parser = BeautifulSoup(html_content, 'html.parser')
    links = parser.find_all('a')

    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)

        if href and href != '#':
            link_info = {
                'href': href,
                'text': text,
                'full_url': f"https://fragment.com{href}"
            }

            links_data.append(link_info)

    collection_name = input("Введите название коллекции подарка: ")
    model = input("Введите интересующая вас модель: ")

    gift = GiftCharacteristics(collection_name, model)

    found_links = []

    if gift.collection_name:
        for link_info in links_data:

            if (gift.collection_name.lower() in link_info['text'].lower() or
                    gift.collection_name.lower() in link_info['href'].lower()):

                found_links.append(link_info)

        if found_links:

            finder_link = []

            link_res = found_links[0]
            finder_link.append(link_res['full_url'])

        else:
            print(f"Ссылки с названием '{gift.collection_name}' не найдены")


find_gift_by_name()