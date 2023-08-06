import webbrowser
from os import environ
from sys import argv
from sys import exit

import requests

__version__ = '2.0.1'

def _sanitize_video_name(video_name:str, video_id:str):
    return video_id

def _get_resolution_from_user(resolutions:dict):
    resolutions_as_list = list(resolutions.keys())
    for index, res in enumerate(resolutions_as_list):
        print(f"{index} - {res}")
    index = int(input("Which resolution (insert number):"))
    return resolutions_as_list[index], resolutions[resolutions_as_list[index]]

def _get_auth_token() -> str:
    token_url_retriever = "https://id.twitch.tv/oauth2/token"
    token_url_retriever_payload = {
        "client_id": environ.get("client_id"),
        "client_secret": environ.get("client_secret"),
        "grant_type": "client_credentials"
    }
    token_url_raw = requests.post(token_url_retriever, data=token_url_retriever_payload)

    return token_url_raw.json().get("access_token")

def get_video_info(video_id: str, video_info_error_handler):
    
    video_info_url = f"https://api.twitch.tv/helix/videos?id={video_id}"
    video_info_header = {
        "Client-Id": environ.get("client_id"),
        "Accept": "application/vnd.twitchtv.v5+json",
        "Authorization": f"Bearer {_get_auth_token()}"
    }
    video_info_raw = requests.get(video_info_url, headers=video_info_header)
    if video_info_raw.status_code != 200:
        print("Error while retrieving video info")
        video_info_error_handler()
    video_info = video_info_raw.json()

    # animated_preview_url contains the domain to retrieve the VOD
    thumbnail_url = video_info.get("data")[0].get("thumbnail_url")
    _ = _sanitize_video_name(video_info.get("title"), video_id)

    if not thumbnail_url:
        print("Error while retrieving video info")
        print(f"thumbnail_url is missing: {video_info}")
        video_info_error_handler()
    return thumbnail_url

def get_video_url(animated_preview_url: str, resolution_name: str):
    domain_parts = animated_preview_url.split("/")
    return f"https://{domain_parts[4]}.cloudfront.net/{domain_parts[5]}/{resolution_name}/index-dvr.m3u8"

def _main():
    try:
        video_id = argv[1]
    except:
        video_id = input("Video ID:")

    # animated_preview_url contains the domain to retrieve the VOD
    animated_preview_url = get_video_info(video_id, lambda: exit(1))
    resolutions = {
        "360p30": "360p30"
    }

    resolution_name, _ = _get_resolution_from_user(resolutions)

    vod_url = get_video_url(animated_preview_url, resolution_name)
    webbrowser.open(vod_url)
