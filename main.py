import discord
from discord.ext import commands

from dotenv import load_dotenv
import os
import json

from steam import Steam
from decouple import config

from collections import OrderedDict

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
    message = """"""
    print("command triggered")
    user_data = steam.users.get_owned_games(username)
    games_list = user_data['games']

    game_dict = OrderedDict()

    for game in games_list:
        game_dict[game['name']] = game['playtime_forever']

    sorted_dict = OrderedDict(sorted(game_dict.items(), key=lambda item: -item[1]))

    for game, playtime in sorted_dict.items():
        time_in_hrs = playtime / 60.0

        length_check = f'{game}: {round(time_in_hrs,1)} hrs'

        if(len(length_check) + len(message) > 2000):
            await ctx.reply(message)
            message = """"""

        message += f'{game}: {round(time_in_hrs,1)} hrs\n'


    await ctx.reply(message)

bot.run(token)
