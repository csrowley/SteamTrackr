import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random

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
async def sendnum(ctx):
    print("Command triggered!")
    await ctx.reply(f'Your number is: {random.randint(0,999)}')

bot.run(token)
