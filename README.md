# RedditBot

A discord bot that takes a Reddit link to a video and combines the video and audio into a single file and sends it back to the Discord server. Cannot usually send videos that are longer than 10-15 seconds due to Discord file limit of 4mb

## Setup

Before using the bot you must create a `.env` file which includes the line `DISCORD_TOKEN=` followed by a discord token.

You will also require `ffmpeg` on your system.
For Debian users, you can run `sudo apt update && sudo apt install -y ffmpeg`

More information on ffmpeg can be found here https://www.ffmpeg.org/.

## .env file
A template/example can be seen below:
```angular2html
DISCORD_TOKEN=""
FFMPEG_LOCATION=""
```
**HOWEVER** the "FFMPEG_LOCATION" variable is not required, if a location is not specified, the bot will use `ffmpeg`.

## Usage

Users can query the bot using the slash commands:

`/reddit <link>` - returns an mp4 of the video \
`/source` - link to GitHub repository \
`/ping` - gets bot latency

## Preview of the bot working

![Preview](https://raw.githubusercontent.com/JoelLucaAdams/RedditBot/master/Preview.png)
