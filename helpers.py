import logging
import os
import subprocess

import discord
import requests

# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

FFMPEG_LOCATION = 'ffmpeg'


def get_reddit_json_payload(url: str):
    try:
        r = requests.get(
            f'{url.split("?", 1)[0]}.json',
            headers={'User-agent': 'redditBot v0.1'}
        )
    except requests.exceptions.RequestException:
        return False, ':warning: Error getting request from url, it may be invalid'

    if r.status_code == 429:
        return False, ':warning: Received error `429` from Reddit'
    else:
        return True, r.json()


def json_payload__get__title(json_payload) -> str:
    return json_payload[0]["data"]["children"][0]["data"]["title"]


def json_payload__get__subreddit(json_payload) -> str:
    return json_payload[0]["data"]["children"][0]["data"]["subreddit_name_prefixed"]


def json_payload__get__video_and_audio(json_payload) -> tuple[str, str]:
    return json_payload[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["fallback_url"], \
           f'{json_payload[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]}/DASH_audio.mp4'


def json__payload__get__gif_or_image(json_payload) -> str:
    return json_payload[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]


def process_media(video, audio) -> bool:
    if requests.get(audio, headers={'User-agent': 'redditBot v0.1'}).status_code != 403:
        process = subprocess.Popen(
            [FFMPEG_LOCATION, '-i', f'{video}', '-i', f'{audio}', '-c', 'copy', 'output.mp4', '-y'],
            cwd=os.getcwd(),
            shell=True,
            stderr=subprocess.PIPE
        )
    else:
        process = subprocess.Popen(
            [FFMPEG_LOCATION, '-i', f'{video}', '-c', 'copy', 'output.mp4', '-y'],
            cwd=os.getcwd(),
            shell=True,
            stderr=subprocess.PIPE
        )

    if process.wait() == 0:
        return True

    logger.log(
        level=logging.CRITICAL,
        msg=process.stderr.read()
    )

    return False


def get_video_url_from_payload(json_payload):
    video, audio = json_payload__get__video_and_audio(json_payload)
    if process_media(video, audio):
        return True, discord.File("output.mp4")
    else:
        return False, None
