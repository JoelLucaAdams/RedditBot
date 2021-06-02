# RedditBot

A discord bot that takes a Reddit link to a video and combines the video and audio into a single file and sends it back to the Discord server. Cannot usually send videos that are longer than 10-15 seconds due to Discord file limit of 4mb

## Setup

Before using the bot you must create a `.env` file which includes the line `DISCORD_TOKEN=` followed by a discord token.

## Usage

Users can query the bot using the slash commands:

`/reddit <link>` - returns an mp4 of the video \
`/source` - link to GitHub repository \
`/ping` - gets bot latency

## Preview of the bot working

![Preview](https://raw.githubusercontent.com/JoelLucaAdams/RedditBot/master/Preview.png)
