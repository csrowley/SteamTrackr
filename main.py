import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json

from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")

steam = Steam(KEY)


load_dotenv()

token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})')
    print("Registered commands:", bot.commands)

@bot.command()
async def myGames(ctx, name):
    message = ""
    print("Command triggered!")
    
    user_data = steam.users.get_owned_games(name)
    games_list = user_data['games']

    for game in games_list:
        if(len(game['name']) + len(message) >= 2000):
            await ctx.send(message)
            message = ""

        message += game['name']
        message += ", \n"

    await ctx.reply(message)

@bot.command()
async def sortByPlaytime(ctx, username):
    return 0

bot.run(token)
