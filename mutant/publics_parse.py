from selenium import webdriver
from PIL import Image
from io import BytesIO
from django.core.cache import cache
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutant.settings')
django.setup()


def parse_publics(player_name):
    # Настройки для браузера
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")  # Открыть окно браузера в максимально возможной ширине

    # Инициализация браузера
    driver = webdriver.Chrome(options=chrome_options)

    # Открытие веб-страницы
    player_name = player_name.lower()
    url = "https://dota2protracker.com/player/" + player_name + "#"
    driver.get(url)

    # Найдите таблицу с классом alx_table sort-fd
    table = driver.find_element('css selector', 'table.alx_table.sort-fd')

    # Найдите заголовок столбца и кликните на него
    header = table.find_element('css selector', 'th.th-mmr')
    header.click()

    # Найдите все строки в таблице
    rows = table.find_elements('css selector', 'tr')
    mmrs = []

    # Объявляем папку для сохранения
    current_path = os.path.dirname(os.path.abspath(__file__))
    subdirectories = ['home', 'static', 'images', 'pub_games']
    for subdir in subdirectories:
        current_path = os.path.join(current_path, subdir)
        if not os.path.exists(current_path):
            os.makedirs(current_path)

    # Перебираем строки таблицы
    for index, row in enumerate(rows):
        if index == 0:
            continue
        # Создаем скриншот для текущей строки
        driver.execute_script("arguments[0].scrollIntoView();", row)
        screenshot = row.screenshot_as_png
        screenshot = Image.open(BytesIO(screenshot))
        width, bottom = screenshot.size
        left, top = 0, 0
        right = width - 630  # Обрезаем справа
        cropped_screenshot = screenshot.crop((left, top, right, bottom))

        # Сохраняем обрезанный скриншот
        screenshot_path = os.path.join(current_path, f"game_{index}.png")
        cropped_screenshot.save(screenshot_path)

        # Сохраняем ммр
        mmrs.append(row.find_element('css selector', 'td.td-mmr').text)

    # Закрытие браузера
    driver.quit()
    cache.set('mmrs', mmrs)


parse_publics('kiyotaka')