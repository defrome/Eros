from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


user_all_links = []


def get_all_gift_links_selenium(collection_name):
    driver = webdriver.Chrome()
    driver.set_window_size(150, 150)

    url = f"https://fragment.com/gifts/{collection_name}?filter=sale"

    driver.get(url)

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-autoscroll-body'))
        )

        last_link_count = 0
        same_count_attempts = 0

        while same_count_attempts < 5:

            grid = driver.find_element(By.CLASS_NAME, 'js-autoscroll-body')


            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", grid)
            time.sleep(1)


            links = grid.find_elements(By.TAG_NAME, 'a')
            current_count = len(links)

            print(f"Найдено ссылок в grid: {current_count}")

            if current_count == last_link_count:
                same_count_attempts += 1
                print(f"Новых ссылок нет ({same_count_attempts}/5)")
            else:
                same_count_attempts = 0
                last_link_count = current_count

            for link in links:
                href = link.get_attribute('href')
                if href and href not in user_all_links:
                    user_all_links.append(href)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

    except TimeoutException:
        print("Таймаут ожидания grid контейнера")
    finally:
        driver.quit()