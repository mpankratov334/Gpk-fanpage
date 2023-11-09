from django.core.cache import cache
import django
import os
import requests


def get_latest_youtube_video(api_key, channel_id):
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'id',
        'channelId': channel_id,
        'order': 'date',
        'maxResults': 5,
        'type': 'video',
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    videos_ids = []
    if 'items' in data and len(data['items']) > 0:
        for i in range(5):
            videos_ids.append('https://www.youtube.com/embed/' + data['items'][i]['id']['videoId'])
    return videos_ids


api_key = 'AIzaSyD0-Gate1FkyuednYJHm_sV5zECpNXLhnc'
channel1_id = 'UCukWhjd4-arDJp3DjxPGXvA'
channel2_id = 'UCkgrCGB_PxFiA-4wVRounlA'


def set_latest_videos_ids():
    latest_videos_ids = get_latest_youtube_video(api_key, channel1_id) + \
                        get_latest_youtube_video(api_key, channel2_id)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutant.settings')
    django.setup()
    cache.set('youtube', latest_videos_ids)


set_latest_videos_ids()
