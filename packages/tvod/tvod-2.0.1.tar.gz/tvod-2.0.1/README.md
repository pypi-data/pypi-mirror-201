# Twitch VOD
Tool to retrieve Twitch's VOD from the video ID

## Install
This package is published on PyPi at this [link](https://pypi.org/project/tvod/). Up to you choose how to install it. 

## Use as is
1. a `client_id` and a `client_secret` are required in order to use this tool. Check [here](https://dev.twitch.tv/console) on how to get them. Set them as environment variables:
  - `export client_id=<YOUR CLIENT ID>`
  - `export client_secret=<YOUR CLIENT SECRET>`

2. Execute the tool from a terminal 
```bash
tvod
```

3. It will ask the video ID (you can find it in twitch's video page). In this (`https://www.twitch.tv/videos/1234567890`) case the ID is `1234567890`

4. It will ask at which resolution watch

5. It will use your browser to watch it.

## Use as package
You can import it in your python script. The available methods are:
- `get_video_info(video_id, video_info_error_handler)`
  - `video_id`: is the id of the twich vod you want to retrieve the info
  - `video_info_error_handler`: is a function (a lambda is good) that will be called if something goes wrong
  - returns the `url` to pass to the fuction `get_video_url`
- `get_video_url(animated_preview_url, resolution_name)`
  - `animated_preview_url`: is the returned url by `get_video_info`
  - `resolution_name`: is the key of the chosen resolution. Some examples are:
    - 360p60
    - 720p60
    - ...
  - return the url to the video at the chosen resolution
