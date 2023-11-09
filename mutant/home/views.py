from django.shortcuts import render
from django.core.cache import cache
from officials_parse import parse_player_results, parse_player_upcoming
from publics_parse import parse_publics
from telegram_parse import set_gpk_channel
from youtube_parse import set_latest_videos_ids


def first_time(request):

    youtube = cache.get('youtube')
    if youtube is None:
        set_latest_videos_ids()
    print('youtube is ready')

    telegram = cache.get('telegram')
    if telegram is None:
        set_gpk_channel()
        telegram = cache.get('telegram')
    print('telegram is ready')

    previous_tournaments = cache.get('previous_tournaments')
    if previous_tournaments is None:
        parse_player_results('Gpk')
        previous_tournaments = cache.get('previous_tournaments')

    upcoming_matches = cache.get('upcoming_matches')
    upcoming_tournaments = cache.get('upcoming_tournaments')
    if upcoming_tournaments is None:
        parse_player_upcoming('Gpk')
        upcoming_matches = cache.get('upcoming_matches')
        upcoming_tournaments = cache.get('upcoming_tournaments')
    mmrs = cache.get('mmrs')
    if mmrs is None and mmrs != []:
        print('MMR not in cache!')
        parse_publics('kiyotaka')
        mmrs = cache.get('mmrs')

    data = {
        'youtube': youtube,
        'telegram': telegram,
        'mmrs': mmrs,
        'range': [f'images/pub_games/game_{i}.png' for i in range(1, len(mmrs) + 1)],
        'upcoming_matches': upcoming_matches,
        'upcoming_tournaments': upcoming_tournaments,
        'previous_tournaments': previous_tournaments,
        'is_mmrs': bool(mmrs)
            }
    print(data)
    return render(request, 'home/main.html', data)
