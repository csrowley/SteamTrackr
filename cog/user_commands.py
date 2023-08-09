from discord.ext import commands
from steam.webapi import WebAPI
from decouple import config
from collections import OrderedDict
from discord import Interaction
from discord import Embed
from discord import app_commands
from apps import emojize

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
                if ceiling <= 0: break

                if(len(game['name']) + len(message) >= 1024):
                    embed.add_field(name = f"Page {count}", value=message, inline=False)
                    message = ""
                    count += 1

                message += game['name']
                message += "\n"

                ceiling -= 1
            embed.add_field(name = f"Page {count}", value=message, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name = "sortbyplaytime", description = "Retrieves user's games in decending order of playtime")
    @app_commands.describe(username = "Enter your steam ID *not the same as username*")
    async def sortbyplaytime(self, interaction: Interaction, username: str, ceiling: int):
        embed = Embed(title = f"{username}'s Sorted Games",  color = 0x774299)
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
            
            count = 1
            for game, playtime in sorted_dict.items():
                time_in_hrs = playtime / 60.0

                length_check = f'{game}: {round(time_in_hrs,1)} hrs'

                if(len(length_check) + len(message) >= 1024):
                    embed.add_field(name = f"Page {count}", value=message, inline=False)
                    count += 1
                    message = """"""

                message += f'{game}: {round(time_in_hrs,1)} hrs\n'

                ceiling -= 1
                if ceiling <= 0: break

            embed.add_field(name = f"Page {count}", value=message, inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"User: '{username}' could not be found.", ephemeral= True)


    @app_commands.command(description = "Display a user's profile")
    @app_commands.describe(user = "Enter your unique steamID or Steam vanityID (custom)")
    async def userprofile(self, interaction: Interaction, user: str):

        if not user.isdigit():
            data = api.call('ISteamUser.ResolveVanityURL', vanityurl = user, url_type = 1)
            user = data['response']['steamid']

        user_summary = api.call('ISteamUser.GetPlayerSummaries', steamids = user)
        user_bans = api.call('ISteamUser.GetPlayerBans', steamids = user)

        user_url = user_summary['response']['players'][0]['profileurl']
        user_persona = user_summary['response']['players'][0]['personaname']
        user_flag = emojize(user_summary['response']['players'][0]['loccountrycode'])

        embed = Embed(title = f"{user_flag} {user_persona}", url = user_url, color = 0x774299)
        embed.set_thumbnail(url = user_summary['response']['players'][0]['avatarfull'])

        embed.add_field(name = f"{user_persona}'s Summary", value = f"**Name:** {user_summary['response']['players'][0]['realname']}\n\n \
                        **SteamID:** {user_summary['response']['players'][0]['steamid']}")
        
        embed.add_field(name = f"{user_persona}'s Bans:", 
                                value = f"**VAC Banned:** {user_bans['players'][0]['VACBanned']}\n\n \
                                **Times VAC Banned:** {user_bans['players'][0]['NumberOfVACBans']}\n\n \
                                **Game Bans:** {user_bans['players'][0]['NumberOfGameBans']} \n\n \
                                **Most Recent Ban:** {user_bans['players'][0]['DaysSinceLastBan']} days\n\n \
                                **Economy Ban:** {user_bans['players'][0]['EconomyBan']}", inline= True)


        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
