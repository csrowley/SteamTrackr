
from discord.ext import commands
from steam.webapi import WebAPI
from decouple import config
from collections import OrderedDict


KEY = config("STEAM_API_KEY")
api = WebAPI(key = KEY)

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def myGames(self, ctx, name):
        message = ""
        try:
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
            if games_list:
                for game in games_list:
                    if(len(game['name']) + len(message) >= 2000):
                        await ctx.reply(message)
                        message = ""

                    message += game['name']
                    message += ", \n"

                await ctx.reply(message)

        except Exception as e:
            await ctx.reply(f"User: '{name}' could not be found.")

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