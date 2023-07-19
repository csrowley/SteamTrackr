import discord
from discord.ext import commands
from discord.ext.commands import is_owner, Context
from dotenv import load_dotenv
from discord import Interaction

from decouple import config

from steam.webapi import WebAPI

from cog.user_commands import UserCog
from cog.game_data import GamesCog

KEY = config("STEAM_API_KEY")
api = WebAPI(key = KEY)

load_dotenv()
token = config("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

#@bot.command()
#@is_owner()
async def setup_cogs():
    user_cog = UserCog(bot)
    games_cog = GamesCog(bot)
    await bot.add_cog(user_cog)
    await bot.add_cog(games_cog)

@bot.event
async def on_ready():
    await setup_cogs()
    print(f'Logged in as {bot.user} ({bot.user.id})')
    print("Registered commands:", bot.commands)


def main():
    bot.run(token)

if __name__ == '__main__':
    main()

