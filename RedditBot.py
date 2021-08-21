import logging
import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

import helpers
from cogs.utilities import Utilities

load_dotenv()

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.default()
)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)


@bot.event
async def on_ready():
    """
    Do something when the bot is ready to use.
    """
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the reddit pages"))


@bot.event
async def on_slash_command_error(ctx, error):
    """
    Handle the Error message in a nice way.
    """
    if hasattr(ctx.command, 'on_error'):
        return
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send(error)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    elif isinstance(error, commands.errors.CommandNotFound):
        pass
    else:
        print(error)
        await ctx.send('An unexpected error occured')
        logging.error(error)


def main():
    if os.getenv('FFMPEG_LOCATION') is not None:
        helpers.FFMPEG_LOCATION = os.getenv('FFMPEG_LOCATION')

    bot.add_cog(Utilities(bot))
    bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    main()
