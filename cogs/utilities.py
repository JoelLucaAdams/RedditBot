import time
from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import SlashContext

import helpers


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
                               'Further development by `Cerys Lewis`\n'
                               'https://github.com/JoelLucaAdams/RedditBot')

    @cog_ext.cog_slash(name="reddit")
    async def _reddit(self, ctx: SlashContext, url: str):
        """
        replies with a video from the reddit link
        """
        await ctx.defer()

        success, json_payload = helpers.get_reddit_json_payload(url)

        if success is False:
            await ctx.send(content=json_payload.get('error-message'))
            return

        embed = Embed(
            description=f'[{json_payload.get("subreddit")} - {json_payload.get("title")}]({url})',
            color=discord.Color.from_rgb(255, 69, 0),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(
            icon_url=ctx.author.avatar_url,
            text=f'Sent by {ctx.author.display_name}'
        )

        is_video, discord_file = helpers.get_video_url_from_payload(json_payload.get('video'), json_payload.get('audio'))
        if is_video is True:
            print(discord_file)
            await ctx.send(embed=embed, file=discord_file)
        else:
            temp_media = json_payload.get('image')
            embed.set_image(url=temp_media)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
