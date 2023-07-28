from discord.ext import commands
from steam.webapi import WebAPI
from decouple import config
from collections import OrderedDict
from discord import Interaction
from discord import Embed
from discord import app_commands

KEY = config("STEAM_API_KEY")
api = WebAPI(key = KEY)

class UserCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("User Commands On")
    

    #add pages to EMBED
    @app_commands.command(name = "mygames", description = "Retrieves all games in users library")
    @app_commands.describe(name = "Enter your steam ID *not the same as username*")
    async def mygames(self, interaction: Interaction, name: str, ceiling: int):
        embed = Embed(title = f"{name}'s Games",  color = 0x774299)
        message = ""
        data = api.call(
            'IPlayerService.GetOwnedGames',
            appids_filter = None,
            include_appinfo=True,
            include_free_sub=False,
            include_played_free_games=True,
            language = 'en',
            include_extended_appinfo = False,
            steamid=name)
        
        games_list = data['response']['games']
        count = 1
        if games_list:
            for game in games_list:
                if(len(game['name']) + len(message) >= 1024):
                    embed.add_field(name = f"Page {count}", value=message, inline=False)
                    message = ""
                    count += 1

                message += game['name']
                message += "\n"

            embed.add_field(name = f"Page {count}", value=message, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @commands.command()
    async def sortByPlaytime(self, ctx, username):
        message = """"""
        try:
            data = api.call(
                'IPlayerService.GetOwnedGames',
                appids_filter = None,
                include_appinfo=True,
                include_free_sub=False,
                include_played_free_games=True,
                language = 'en',
                include_extended_appinfo = False,
                steamid=username)
            
            games_list = data['response']['games']

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

        except Exception as e:
            await ctx.reply(f"User: '{username}' could not be found.")


    @app_commands.command(description = "Display a user's profile")
    async def userprofile(self, interaction: Interaction, user: str):
        user_summary = api.call('ISteamUser.GetPlayerSummaries', steamid = user)
        user_bans = api.call('ISteamUser.GetPlayerBans', steamid = user)


        return
    '''
    GetPlayerSummaries
    GetPlayerBans
    '''

    #DB method
    @commands.command()
    async def myWishlist(self, ctx, user):
        return
    
    #DB method
    @commands.command()
    async def addWishlist(self, ctx, user, title):
        return
    
    #DB method
    @commands.command()
    async def removeWishlist(self, ctx, user, title):
        return
    

    #add functionality where user can enter private message in DMs
