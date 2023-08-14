from discord.ext import commands
from steam.webapi import WebAPI
from discord import Interaction
from discord import Embed
from discord import app_commands

from apps import emojize, game_info
import sqldb.wishlist

class MyWishlist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "mywishlist", description = "Retrieves all entries in your wishlist.")
    async def mywishlist(self, interaction: Interaction):
        userWishlist = sqldb.wishlist.get_wish_by_user(interaction.user.name)
            
        if userWishlist:
            print(userWishlist)
        else:
            print(interaction.user.name)
            await interaction.response.send_message("No wishlist found", ephemeral=True)
        
    #DB method
    @app_commands.command(name = "addwishlist", description = "Add a game title to your wishlist.")
    @app_commands.describe(title = "Enter game title with exact spelling")
    async def addwishlist(self, interaction: Interaction, title: str):
        details = game_info(title)

        try:
            newList = sqldb.wishlist.Wishlist(user=interaction.user.name, title= title, price= details["initial"], link= details["link"])
            userCount = sqldb.wishlist.number_entries_from_user(interaction.user.name)
            if userCount >= 150:
                await interaction.response.send_message("Wishlist exceeds max limit of entries.", ephemeral=True)
                return
            
            sqldb.wishlist.insert_wish_list(newList)
            await interaction.response.send_message("Successfully added to wishlist.", ephemeral=True)

        except Exception as e :
            await interaction.response.send_message("Something went wrong. Make sure the spelling is correct.", ephemeral=True)
            return
        
        
        
    #DB method
    @commands.command()
    async def removewishlist(self, interaction: Interaction, user, title):
        return