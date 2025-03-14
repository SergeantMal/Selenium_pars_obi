import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

parsed_data = []

base_url = "https://obi.ru/osveschenie?page="
current_page = 1
MAX_PAGES = 69  # Лимит страниц

while current_page <= MAX_PAGES:
    next_page_url = f"{base_url}{current_page}"  # Формируем URL следующей страницы
    print(f"Скрейпинг страницы: {next_page_url}")

    driver.get(next_page_url)  # Открываем страницу
    time.sleep(1)  # Даем странице загрузиться

    # Находим товары
    svet = driver.find_elements(By.CSS_SELECTOR, 'div._3yNpa div.FuS7R')

    for svet_item in svet:
        try:
            name = svet_item.find_element(By.CSS_SELECTOR, 'p._1UlGi').text
            price = svet_item.find_element(By.CSS_SELECTOR, 'div._1YQve span').text
            link_element = svet_item.find_element(By.CSS_SELECTOR, 'a')
            link = link_element.get_attribute('href') if link_element else None

            # Убираем неразрывные пробелы в цене
            price = price.replace("\xa0", "")

        except Exception as e:
            print(f"Произошла ошибка при парсинге: {e}")
            continue

        parsed_data.append([name, price, link])

    current_page += 1  # Увеличиваем номер страницы



driver.quit()

with open("catalog.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название товара', 'Цена', 'Ссылка на товар'])
    writer.writerows(parsed_data)