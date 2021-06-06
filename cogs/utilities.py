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
        
        try:
            r = requests.get(f'{url.split("?", 1)[0]}.json', headers={'User-agent': 'redditBot v0.1'})
        except requests.exceptions.RequestException:
            await ctx.send(":warning: Error getting request from url, it may be invalid")
            return

        if r.status_code == 429:
            await ctx.send("Recieved error `429` from Reddit")
            return
        else:
            json_response = r.json()
    
        title = json_response[0]["data"]["children"][0]["data"]["title"]
        subreddit = json_response[0]["data"]["children"][0]["data"]["subreddit_name_prefixed"]

        embed = Embed(description=f'[{subreddit} - {title}]({url})', color=discord.Color.from_rgb(255, 69, 0), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=ctx.author.avatar_url, text= f'Sent by {ctx.author.display_name}')

        # Checks if the video url exists
        try:
            video = json_response[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["fallback_url"]

            audio = f'{json_response[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]}/DASH_audio.mp4'

            if requests.get(audio, headers={'User-agent': 'redditBot v0.1'}).status_code != 403:
                p1 = subprocess.Popen(['ffmpeg', '-i', f'{video}', '-i', f'{audio}', '-c', 'copy', 'output.mp4', '-y'], cwd=os.getcwd())
            else:
                p1 = subprocess.Popen(['ffmpeg', '-i', f'{video}', '-c', 'copy', 'output.mp4', '-y'], cwd=os.getcwd())
            
            p1.wait()
            await ctx.send(embed=embed, file=discord.File("output.mp4"))
            return
        except TypeError:
            pass

        # Checks if the video url exists with a crosspost
        try:
            video = json_response[0]["data"]["children"][0]["data"]["crosspost_parent_list"][0]["secure_media"]["reddit_video"]["fallback_url"]

            audio = f'{json_response[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]}/DASH_audio.mp4'

            if requests.get(audio, headers={'User-agent': 'redditBot v0.1'}).status_code != 403:
                p1 = subprocess.Popen(['ffmpeg', '-i', f'{video}', '-i', f'{audio}', '-c', 'copy', 'output.mp4', '-y'], cwd=os.getcwd())
            else:
                p1 = subprocess.Popen(['ffmpeg', '-i', f'{video}', '-c', 'copy', 'output.mp4', '-y'], cwd=os.getcwd())
            
            p1.wait()
            await ctx.send(embed=embed, file=discord.File("output.mp4"))
            return
        except KeyError:
            pass

        # Checks if there is a gif or an image
        try:
            img_or_gif = json_response[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]
            embed.set_image(url=img_or_gif)
            await ctx.send(embed=embed)
        except TypeError:
            pass
                
def setup(bot):
    bot.add_cog(Utilities(bot))