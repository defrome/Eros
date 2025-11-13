import asyncio
import requests
from db.database import create_database
from bs4 import BeautifulSoup
asyncio.run(create_database())

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


            print(f"Ссылка: {link_info['full_url']}")
            print(f"Текст: {link_info['text']}")
            links_data.append(link_info)

    collection_name = input("Введите название коллекции подарка: ")
    model = input("Введите интересующая вас модель: ")

    gift = GiftCharacteristics(collection_name, model)
    print(gift.collection_name, gift.model)


find_gift_by_name()