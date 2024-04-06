from flask import current_app
import requests

def return_url(query):
    api_key = current_app.config["YOUTUBE_API_KEY"]
    url = ('https://youtube.googleapis.com/youtube/v3/search?'\
                        'part=snippet&'\
                        'maxResults=1&'\
                        'order=relevance&'\
                        f'q=medical first aid for {query}&'\
                        'type=video&'\
                        'videoDuration=short&'\
                        'videoEmbeddable=true&'\
                        f'key={api_key}')
    response = requests.get(url)
    if response.status_code == 200:
        data =  response.json()['items']
        url_links = {data[i]['snippet']['title']:f"https://youtu.be/{data[i]['id']['videoId']}" for i in range(len(data))}
        return url_links
    return False