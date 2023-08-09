from discord.ext import commands
from steam.webapi import WebAPI
from discord import Interaction
from discord import Embed
from discord import app_commands
from apps import emojize
import sqldb.wishlist

class Wishlist:
    def __init__(self, user, title, price, link):
        self.user = user
        self.title = title
        self.price = price
        self.link = link

    @commands.command()
    async def myWishlist(self, ctx, user):
        return
    
    #DB method
    @commands.command()
    async def addWishlist(self, interaction: Interaction, user, title):
        return
    
    #DB method
    @commands.command()
    async def removeWishlist(self, interaction: Interaction, user, title):
        return