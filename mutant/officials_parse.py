import requests
from django.core.cache import cache
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutant.settings')
django.setup()


def parse_player_results(player_name):
    url = f"https://liquipedia.net/dota2/{player_name}/Results"
    # Отправляем GET-запрос на указанный URL
    response = requests.get(url)
    results = []
    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # Находим таблицу с результатами игрока
        results_table = soup.find("table", {"class": "wikitable"})

        # Если таблица найдена, можно извлечь информацию
        if results_table:
            rows = results_table.find_all("tr")
            tournaments_count = 0
            for row in rows:
                columns = row.find_all("td")
                match = {}
                if len(columns) >= 3:
                    tournaments_count += 1
                    date = columns[0].text.strip()
                    if int(date[:4]) < datetime.now().year or tournaments_count > 4:
                        break
                    place = columns[1].text.strip()
                    tier = columns[2].text.strip()
                    tournament = columns[4].text.strip()
                    link = r'https://liquidpedia.net' + columns[4].find("a")["href"]

                    # Выводим информацию о каждом матче
                    match["date"] = date
                    match["place"] = place.replace('\xa0', '')
                    match["tier"] = tier
                    match["name"] = tournament
                    match["url"] = link
                    results.append(match)
        else:
            print("Таблица результатов не найдена.")
    else:
        print("Не удалось получить доступ к странице.")

    cache.set('previous_tournaments', results)
    return results


def parse_player_upcoming(player_name):
    # Формируем URL-адрес страницы с информацией об игроке
    url = f"https://liquipedia.net/dota2/{player_name}"
    # Отправляем GET-запрос на страницу
    upcoming_matches = []
    response = requests.get(url)
    if response.status_code == 200:
        # Используем BeautifulSoup для парсинга HTML-кода страницы
        soup = BeautifulSoup(response.content, 'html.parser')

        # Найдем таблицу с предстоящими матчами игрока
        tables = soup.find_all('div', class_="fo-nttax-infobox wiki-bordercolor-light")

        # Проходимся по каждому матчу
        for row in tables[0].find_all('table'):
            match = {}
            # Извлекаем информацию из нужных ячеек
            team1 = row.find('td', class_="team-left").text.strip()
            team2 = row.find('td', class_="team-right").text.strip()
            date = row.find('span', class_="match-countdown").text.strip()
            date = convert_datetime_string(date)

            # Выводим информацию о матче
            match["date"] = date
            match["team1"] = team1
            match["team2"] = team2
            upcoming_matches.append(match)
        # Найдем блок с предстоящими турнирами игрока
        upcoming_tournaments_block = tables[1]
        upcoming_tournaments = []
        if upcoming_tournaments_block:
            # Найдем ссылки на предстоящие турниры
            for table in upcoming_tournaments_block.find_all('table',
                                                        class_="wikitable wikitable-striped infobox_matches_content"):
                tournament = {}
                tournament_name = table.find('td').text.strip()
                tournament_date = table.find('div').text.strip()
                tournament_url = table.find('a')['href']

                # Выводим информацию о турнире
                tournament["name"] = tournament_name
                tournament["date"] = tournament_date
                tournament["url"] = f'https://liquidpedia.net{tournament_url}'
                upcoming_tournaments.append(tournament)
        else:
            print("Предстоящие турниры не найдены.")
    else:
        print("Ошибка при получении страницы.")
    cache.set('upcoming_matches', upcoming_matches)
    cache.set('upcoming_tournaments', upcoming_tournaments)
    return upcoming_matches, upcoming_tournaments


def convert_datetime_string(datetime_string):
    # Определение словаря с соответствиями названий месяцев на русском языке
    month_names = {
        'January': 'января',
        'February': 'февраля',
        'March': 'марта',
        'April': 'апреля',
        'May': 'мая',
        'June': 'июня',
        'July': 'июля',
        'August': 'августа',
        'September': 'сентября',
        'October': 'октября',
        'November': 'ноября',
        'December': 'декабря'
    }

    # Преобразование строки в объект datetime
    datetime_obj = datetime.strptime(datetime_string, "%B %d, %Y - %H:%M %Z")

    # Добавление 3 часов к времени
    datetime_obj += timedelta(hours=3)

    # Получение названия месяца на русском языке
    month = month_names.get(datetime_obj.strftime('%B'), '')

    # Формирование результирующей строки
    result_string = datetime_obj.strftime(f"%d {month} %H:%M")

    return result_string

player_name = "Gpk"
upcoming = parse_player_upcoming(player_name)
previous = parse_player_results(player_name)
