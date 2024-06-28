# import queue
# import logging
#
# import discord
# from discord import app_commands
# from discord.ext import commands
#
# from theta.utils import thetacolors
#
#
# #  from data import ScrimsDB
#
# class Scrim(commands.Cog):
#     def __int__(self, bot: commands.Bot):
#         self.bot = bot
#
#     @app_commands.command(name="scrim-new", description="Create a new scrim post and add it to the board")
#     @app_commands.guild_only
#     @app_commands.describe(team_name="What is the name of your team?")
#     @app_commands.describe(results_or_division="How much experience do you have playing Splatoon? Eg, CCA Division 3, LUTI Division 7, #th place in a tournament, # rank average in solo queue (for players without results)")
#     @app_commands.describe(time_and_map_list="What time do you want to find a scrim for? Do you have a map list in mind or would 'any maps' do? Heads up! Timestamps are preferred here! You can make one with /timestamp.")
#     @app_commands.describe(screen_OK="Does your team need to ban splattercolor screen due to any issues it causes?")
#     @app_commands.choices(screen_banned=[
#         discord.app_commands.Choice(name="Screen is OK", value=1),
#         discord.app_commands.Choice(name="Screen is NOT PERMITTED.", value=1)
#     ])
#     async def scrim(self, interaction: discord.Interaction):