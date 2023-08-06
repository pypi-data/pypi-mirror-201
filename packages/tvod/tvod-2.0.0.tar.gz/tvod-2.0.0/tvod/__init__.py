from sys import exit, argv
import webbrowser

import requests

__version__ = '1.1.0'

def _sanitize_video_name(video_name:str, video_id:str):
    return video_id

def _get_resolution_from_user(resolutions:dict):
    resolutions_as_list = list(resolutions.keys())
    for index, res in enumerate(resolutions_as_list):
        print(f"{index} - {res}")
    index = int(input("Which resolution (insert number):"))
    return resolutions_as_list[index], resolutions[resolutions_as_list[index]]

def get_video_info(video_id: str, video_info_error_handler):
    video_info_url = f"https://api.twitch.tv/kraken/videos/{video_id}"
    video_info_header = {
        "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
        "Accept": "application/vnd.twitchtv.v5+json"
    }
    video_info = requests.get(video_info_url, headers=video_info_header).json()

    # animated_preview_url contains the domain to retrieve the VOD
    animated_preview_url = video_info.get("animated_preview_url")
    resolutions = video_info.get("resolutions")
    _ = _sanitize_video_name(video_info.get("title"), video_id)

    if not animated_preview_url or not resolutions:
        print("Error while retrieving video info")
        video_info_error_handler()

    return animated_preview_url, resolutions

def get_video_url(animated_preview_url: str, resolution_name: str):
    domain_parts = animated_preview_url.split("/")
    return f"https://{domain_parts[2]}/{domain_parts[3]}/{resolution_name}/index-dvr.m3u8"

def _main():
    try:
        video_id = argv[1]
    except:
        video_id = input("Video ID:")

    # animated_preview_url contains the domain to retrieve the VOD
    animated_preview_url, resolutions = get_video_info(video_id, lambda: exit(1))
    if not animated_preview_url or not resolutions:
        print("Error while retrieving video info")
        exit(1)

    resolution_name, _ = _get_resolution_from_user(resolutions)

    vod_url = get_video_url(animated_preview_url, resolution_name)
    webbrowser.open(vod_url)

