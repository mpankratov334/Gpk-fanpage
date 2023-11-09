from googleapiclient.discovery import build

# Replace with your API key
api_key = 'AIzaSyAa-HYMifgnr906xHIUsNq34xB98Gq9-NI'

# YouTube channels IDs
esport_channel_id = 'UCukWhjd4-arDJp3DjxPGXvA'
team_channel_id = 'UCkgrCGB_PxFiA-4wVRounlA'

# The tag to filter by (e.g., "gpk")
tag = 'dota'


def filter_videos_with_tag(videos, tag):
    filtered = []
    for video in videos:
        if 'tag' not in video['snippet']['tags']:
            continue
        filtered.append(video)
        if len(filtered) == 5:
            break
    return filtered


# Function to search for videos by tag and channel
def search_videos(api, channel_id, search_query):
    search_response = api.search().list(
        q='dota',
        channelId=channel_id,
        type='video',
        part='id,snippet',
        order='date',
    ).execute()
    print(search_response)
    return search_response.get('items', [])


def print_videos_info_from_channel(channel_id):
    # Create a YouTube Data API service instance
    youtube = build('youtube', 'v3', developerKey=api_key)
    print(type(youtube))

    for video in filter_videos_with_tag(search_videos(youtube, channel_id, tag), tag):
        title = video['snippet']['title']
        video_id = video['id']['videoId']

        # Get video details by video ID
        video_response = youtube.videos().list(
            id=video_id,
            part='contentDetails'
        ).execute()

        # Check for age restriction
        age_restricted = 'contentRating' in video_response['items'][0]['contentDetails']

        print(f'Title: {title}')
        print(f'Video ID: {video_id}')
        print(f'Is Age Restricted: {age_restricted}')
        print('---')


if __name__ =='__main__':
    print_videos_info_from_channel(esport_channel_id)
    print_videos_info_from_channel(team_channel_id)

