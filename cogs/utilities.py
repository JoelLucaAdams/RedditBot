import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed
import time
import subprocess
import requests
import os
from datetime import datetime


class Utilities(commands.Cog):
    """
    General Utilities
    """

    @commands.command()
    async def ping(self, ctx: Context):
        """
        Status check
        """
        start_time = time.time()
        message = await ctx.send('pong. `DWSPz latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms`')
        end_time = time.time()
        await message.edit(content='pong. `DWSP latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms` ' +
                                   '`Response time: ' + str(int((end_time - start_time) * 1000)) + 'ms`')

    @commands.command()
    async def source(self, ctx: Context):
        """
        Print a link to the source code
        """
        await ctx.send(content='Created by `Joel Adams`\n'
                               'https://github.com/JoelLucaAdams/RedditBot')

    @commands.command()
    async def reddit(self, ctx: Context, url: str):
        """
        Replies with man page message
        """
        await ctx.message.delete()

        r = requests.get(f'{url.split("?", 1)[0]}.json', headers= {'User-agent': 'redditBot v0.1'})

        if r.status_code == 429:
            await ctx.send("Recieved error `429` from Reddit")
            return
        else:
            json_response = r.json()

        video = json_response[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["fallback_url"]
        audio = f'{json_response[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]}/DASH_audio.mp4'

        title = json_response[0]["data"]["children"][0]["data"]["title"]
        subreddit = json_response[0]["data"]["children"][0]["data"]["subreddit_name_prefixed"]
        #url = json_response[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]

        if requests.get(audio, headers={'User-agent': 'redditBot v0.1'}).status_code != 403:
            p1 = subprocess.Popen(['ffmpeg', '-i', f'{video}', '-i', f'{audio}', '-c', 'copy', 'output.mp4', '-y'], cwd=os.getcwd())
        else:
            p1 = subprocess.Popen(['ffmpeg', '-i', f'{video}', '-c', 'copy', 'output.mp4', '-y'], cwd=os.getcwd())
        
        p1.wait()
        #await ctx.send(file=discord.File("output.mp4"))
        

        #await ctx.send('Compressing video...')
        #p2 = subprocess.Popen(['ffmpeg', '-i', 'output.mp4', '-vcodec', 'libx265', '-crf', '24', 'compressed.mp4', '-y'], cwd=os.getcwd())
        #p2.wait()

        embed = Embed(description=f'[{subreddit} - {title}]({url})', color=discord.Color.from_rgb(255, 69, 0), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=ctx.author.avatar_url, text= f'Sent by {ctx.author.display_name}')
        #embed.set_image(url="optput.mp4") yuntgifgkimu yh0i66555
        await ctx.send(embed=embed, file=discord.File("output.mp4"))

    @reddit.error
    async def reddit_error(self, ctx, error):
        await ctx.send(error)