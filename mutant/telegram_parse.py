from telethon.sync import TelegramClient
from django.core.cache import cache
import django
import os

API_ID = '25146138'
API_HASH = 'ec74051b29bbbcb7d0e0f50c63e33745'
channel = 'gpk_dota2'


# объявляем папку для сохранения
def path_creator():
    current_path = os.path.dirname(os.path.abspath(__file__))
    subdirectories = ['home', 'static', 'telegram']
    for subdir in subdirectories:
        current_path = os.path.join(current_path, subdir)
        if not os.path.exists(current_path):
            os.makedirs(current_path)
    return current_path


def set_gpk_channel():
    telegram_data = parse_gpk_channel()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutant.settings')
    django.setup()
    cache.set('telegram', telegram_data)


def parse_gpk_channel():
    client = TelegramClient('gpk', API_ID, API_HASH, system_version='4.16.30-vxa')
    current_path = path_creator()
    client.connect()
    client.start()
    tg_data = []
    for mes_num, message in enumerate(client.iter_messages(channel, limit=10), start=1):
        new_mes = {}
        if message.video:
            video = message.video
            video_path = os.path.join(current_path, f'{mes_num}.mp4')
            message.download_media(file=video_path)
            new_mes['video'] = os.path.join('telegram', f'{mes_num}.mp4')

        if message.text:
            new_mes['txt'] = message.text

        if message.photo:
            photo_path = os.path.join(current_path, f'{mes_num}.jpg')
            message.download_media(file=photo_path)
            new_mes['img'] = os.path.join('telegram', f'{mes_num}.jpg')

        tg_data.append(new_mes)
    client.disconnect()
    return tg_data


set_gpk_channel()
print(cache.get('telegram'))