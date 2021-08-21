import discord
from discord.ext import commands
from discord_slash import SlashCommand
from cogs.utilities import Utilities
import os
import logging
from dotenv import load_dotenv


# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# load the private discord token from .env file.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.default()
)

slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

# Setup cogs
bot.add_cog(Utilities(bot))


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
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
