import discord
from discord import Embed
from discord.ext import commands
from discord_slash.context import SlashContext
from discord_slash import cog_ext, error
import time
import subprocess
import requests
import os
from datetime import datetime

from helpers import get_reddit_json_payload, json_payload__get__title, json_payload__get__subreddit, \
    json_payload__get__video_and_audio, process_media, get_video_url_from_payload, json__payload__get__gif_or_image


class Utilities(commands.Cog):
    """
    General Utilities
    """

    @cog_ext.cog_slash(name="ping")
    async def _ping(self, ctx: SlashContext):
        """
        Status check
        """
        start_time = time.time()
        message = await ctx.send('pong. `DWSPz latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms`')
        end_time = time.time()
        await message.edit(content='pong. `DWSP latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms` ' +
                                   '`Response time: ' + str(int((end_time - start_time) * 1000)) + 'ms`')

    @cog_ext.cog_slash(name="source")
    async def _source(self, ctx: SlashContext):
        """
        Print a link to the source code
        """
        await ctx.send(content='Created by `Joel Adams`\n'
                               'https://github.com/JoelLucaAdams/RedditBot')

    @cog_ext.cog_slash(name="reddit")
    async def _reddit(self, ctx: SlashContext, url: str):
        """
        replies with a video from the reddit link
        """
        await ctx.defer()
        
        success, json_payload = get_reddit_json_payload(url)

        if success is False:
            await ctx.send(content=json_payload)
            return

        title = json_payload__get__title(json_payload)
        subreddit = json_payload__get__subreddit(json_payload)

        embed = Embed(
            description=f'[{subreddit} - {title}]({url})',
            color=discord.Color.from_rgb(255, 69, 0),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(
            icon_url=ctx.author.avatar_url,
            text=f'Sent by {ctx.author.display_name}'
        )

        is_video, discord_file = get_video_url_from_payload(json_payload)
        if is_video is True:
            await ctx.send(embed=embed, file=discord_file)
        else:
            temp_media = json__payload__get__gif_or_image(json_payload)
            embed.set_image(url=temp_media)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
