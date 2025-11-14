import sqlite3
import requests
from bs4 import BeautifulSoup
from config import DB_URL
from db.database import db_func
from driver_script import get_all_gift_links_selenium, user_all_links

# создаем бд для информации о пользователе
db_func()


# стартовое сообщение
def print_banner(script_name, description=""):  # Убрал -> str, так как функция ничего не возвращает
    print("\n" + "=" * 50)
    print(f"{script_name}")
    print("=" * 50)
    if description:
        print(f"{description}")
    print("Скрипт успешно запущен!")
    print("=" * 50 + "\n")


print_banner(
    "Eros tracker",
    "Telegram nft gifts tracker"
)

try:
    res = requests.get('https://fragment.com/gifts')
    res.raise_for_status()
    html_content = res.text
except requests.RequestException as e:
    print(f"Ошибка при получении страницы: {e}")
    html_content = ""


links_data = []


class GiftCharacteristics:
    def __init__(self, collection_name, model_id):
        self.collection_name = collection_name
        self.model_id = model_id


def find_gift_by_name():
    if not html_content:
        print("Ошибка: не удалось получить содержимое страницы")
        return

    parser = BeautifulSoup(html_content, 'html.parser')
    links = parser.find_all('a')

    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)

        if href and href != '#':
            full_url = f"https://fragment.com{href}" if href.startswith('/') else href
            link_info = {
                'href': href,
                'text': text,
                'full_url': full_url
            }
            links_data.append(link_info)

    collection_name = "diamondring"
    model_id = 28934

    gift = GiftCharacteristics(collection_name, model_id)

    print(gift.collection_name)

    get_all_gift_links_selenium(collection_name)

    print(user_all_links)

    if user_all_links:

        user_model_url = f"https://fragment.com/gift/{collection_name}-{model_id}?filter=sale"

        current_link = []

        if user_model_url in user_all_links:

            current_link.append(user_model_url)

            try:
                with sqlite3.connect(DB_URL) as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_info SET last_gift = ?", (user_model_url,))
                    conn.commit()

            except sqlite3.Error as e:
                print(f"Ошибка базы данных: {e}")

        else:

            print("Ссылка не найдена.")

    try:
        with sqlite3.connect(DB_URL) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE user_info SET value = value + 1")
            conn.commit()

    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")


find_gift_by_name()