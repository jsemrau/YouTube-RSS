from googleapiclient.discovery import build
import os,json, feedparser
from dotenv import load_dotenv

load_dotenv()
gApiKey = os.getenv('GOOGLE_API_KEY')

def get_channel_id(api_key, channel_name):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Search for the channel using the channel name
    search_response = youtube.search().list(
        q=channel_name,
        part='id',
        maxResults=1,
        type='channel'
    ).execute()

    # Extract the channel ID from the search response
    channel_id = search_response['items'][0]['id']['channelId']
    return channel_id

def parse_youtube_rss(channel_url):
    feed = feedparser.parse(channel_url)

    videos = []
    for entry in feed.entries:
        video = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'description': entry.summary,
        }
        videos.append(video)

    return videos

#Main executes the script
if __name__ == '__main__':

    yters = ['materialimpacts']

    # Replace 'YOUR_CHANNEL_URL' with the URL of the YouTube channel's RSS feed
    channel_id = get_channel_id(gApiKey, yters[0])
    channel_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
    videos = parse_youtube_rss(channel_url)

    # Convert the videos list to JSON
    json_data = json.dumps(videos, indent=4)

    # Print the JSON data
    print(json_data)
