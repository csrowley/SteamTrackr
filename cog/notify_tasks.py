from discord.ext import tasks, commands
from steam.webapi import WebAPI
from decouple import config
from discord import Interaction, Embed, app_commands
from bs4 import BeautifulSoup
from apps import checkSaleEvents
import datetime
import pytz

class Notifiers(commands.Cog):

    _pst = pytz.timezone('US/Pacific')
    _time = datetime.time(hour= 17, minute=30)
    def __init__(self, bot):
        self.bot = bot
        self.on_steam_event_sale.start()

    def cog_unload(self):
        self.on_steam_event_sale.cancel()

    #possibly use "on_scheduled_event" ?
    #scrape the steam official news tab for possible sales
    @commands.command()
    async def setEventReminder(self,ctx, switch):
        pass
    
    
    #fix not working
    @tasks.loop(time = _time)
    async def on_steam_event_sale(self):
        print("Executing:")
        checkevent = checkSaleEvents()

        if not checkevent: return

        for guild in self.bot.guilds:
            if guild.system_channel:
                await guild.system_channel.send(checkevent)
            
    #DB method
    @commands.Cog.listener()
    async def on_game_sale(self,ctx,user,title):
        print("")

    @app_commands.command(description = "Checks for any major Steam Sales")
    async def checksaleevents(self, interaction: Interaction):
        checkevent = checkSaleEvents()

        if checkevent:
            await interaction.response.send_message(checkevent)
        else:
            await interaction.response.send_message("No major sale event.")

