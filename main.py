import sqlite3

import requests

from bs4 import BeautifulSoup

from config import DB_URL
from db.database import db_func

# создаем бд для информации о пользователе
db_func()


# стартовое сообщение
def print_banner(script_name, description="") -> str:
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

            finder_link = found_links[0]['full_url']
            print(f"Найдена ссылка: {finder_link}")

            gifts_res = requests.get(finder_link)
            html_content_gifts = gifts_res.text

            parser_gifts = BeautifulSoup(html_content_gifts, 'html.parser')
            gifts = parser_gifts.find_all('a')

            gifts_data = []

            for gift_link in gifts:

                href = gift_link.get('href')
                text = gift_link.get_text(strip=True)

                if (href and href != '#' and
                        href.startswith('/gift/') and
                        '-' in href and
                        href.split('-')[-1].isdigit()):

                    gift_info = {
                        'href': href,
                        'text': text,
                        'full_url': f"https://fragment.com{href}"
                    }

                    gifts_data.append(gift_info)
                    print(gift_info)

            try:
                with sqlite3.connect(f"{DB_URL}") as conn:
                    cursor = conn.cursor()

                    cursor.execute("UPDATE user_info SET value = value + 1")
                    conn.commit()

            except sqlite3.Error as e:
                print(f"Ошибка базы данных: {e}")

        else:
            print(f"Ссылки с названием '{gift.collection_name}' не найдены")


find_gift_by_name()