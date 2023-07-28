from discord.ext import tasks, commands
from steam.webapi import WebAPI
from decouple import config
from discord import Interaction, Embed, app_commands
import asyncpg
from bs4 import BeautifulSoup
import requests
import datetime

class Notifiers(commands.Cog):

    _utc = datetime.timezone.utc
    _time = datetime.time(hour= 17, minute=30, tzinfo=_utc)
    
    def init(self, bot):
        self.bot = bot

    def cog_unload(self):
        pass

        #possibly use "on_scheduled_event" ?
    #scrape the steam official news tab for possible sales
    @commands.command()
    async def setEventReminder(self,ctx, switch):
        return


    @tasks.loop(time=_time)
    async def on_steam_event_sale(self):
        pass #add in checksaleevents
            
    #DB method
    @commands.Cog.listener()
    async def on_game_sale(self,ctx,user,title):
        print("")

    @app_commands.command(description = "Checks for any major Steam Sales")
    async def checksaleevents(self, interaction: Interaction):
        all_sales = {"steam spring sale", "steam summer sale", "steam autumn sale", "steam winter sale", "halloween"}
        url = "https://store.steampowered.com/"
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, "html.parser")
        meta_desc = soup.find("meta", property="og:description")

        if meta_desc:
            desc = meta_desc["content"].lower()
            for sales in all_sales:
                if sales in desc:
                    await interaction.response.send_message(sales.title())
                    return
                
            await interaction.response.send_message("No major sale event.")

