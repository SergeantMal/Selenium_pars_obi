import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройки браузера (headless режим)
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # Скрытый режим
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

# Базовый URL
base_url = "https://obi.ru/osveschenie?page="
current_page = 1

# Открываем CSV-файл
with open("catalog.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название товара', 'Цена', 'Ссылка на товар'])  # Заголовки

    while True:  # Цикл по страницам
        next_page_url = f"{base_url}{current_page}"
        print(f"Скрейпинг страницы: {next_page_url}")
        driver.get(next_page_url)

        # Проверяем, есть ли текст ошибки 404
        if "404 This page could not be found." in driver.page_source:
            print(f"Страница {current_page} не существует (404). Останавливаем парсинг.")
            break

        # Ждем загрузки товаров
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div._3yNpa div.FuS7R'))
            )
        except:
            print(f"Страница {current_page} пуста. Останавливаем парсинг.")
            break  # Если товаров нет – выходим из цикла

        # Находим товары
        svet = driver.find_elements(By.CSS_SELECTOR, 'div._3yNpa div.FuS7R')

        for svet_item in svet:
            try:
                name = svet_item.find_element(By.CSS_SELECTOR, 'p._1UlGi').text
                price = svet_item.find_element(By.CSS_SELECTOR, 'div._1YQve span').text
                link = svet_item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

                price = price.replace("\xa0", "")  # Чистим цену

                writer.writerow([name, price, link])  # Записываем данные в файл

            except Exception as e:
                print(f"Ошибка при обработке товара: {e}")

        current_page += 1  # Переход на следующую страницу

# Закрываем браузер
driver.quit()
print("Парсинг завершен, данные сохранены в catalog.csv")