import pandas as pd
import re
from googleapiclient.discovery import build

API_KEY = 'insert key'
MTG_GOLDFISH_CHANNEL_ID = 'UCZAZTSd0xnor7hJFmINIBIw'
video_times = {'Standard': ['00:00:00 Thursday', '12:12:12 Friday'], 'Modern': ['00:00:00 Thursday', '12:12:12 Friday']}

api_service_name = "youtube"
api_version = "v3"

youtube = build(api_service_name, api_version, developerKey=API_KEY)

request = youtube.channels().list(
    part = "snippet,contentDetails,statistics",
    id = MTG_GOLDFISH_CHANNEL_ID
)
response = request.execute()


uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


request = youtube.playlists().list(
    part="snippet",
    channelId=MTG_GOLDFISH_CHANNEL_ID,
    maxResults=50
)
response = request.execute()

budget_magic_playlist_id = None
for item in response['items']:
    if item['snippet']['title'] == 'Budget Magic':
        budget_magic_playlist_id = item['id']
        break

if not budget_magic_playlist_id:
    print("Budget Magic playlist not found.")
    exit()

video_details = []
next_page_token = None

while True:
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,  # max allowed by API
        playlistId=budget_magic_playlist_id,
        pageToken=next_page_token
    )
    response = request.execute()

    for item in response['items']:
        title = item['snippet']['title']
        description = item['snippet']['description']
        if 'Modern' in title:
            url_match = re.search(r'latest prices: (https://www\.mtggoldfish\.com/deck/[^\s]+)', description)
            if url_match:
                details = {
                    # 'title': title,
                    'publishedAt': item['snippet']['publishedAt'],
                    'deck_url': url_match.group(1)
                }
                video_details.append(details)

    next_page_token = response.get('nextPageToken')
    if not next_page_token:
        break


df = pd.DataFrame(video_details)
df.to_csv('budget_magic_video_details.csv', index=False)
