import queue
import logging

import discord
from discord import app_commands
from discord.ext import commands

from theta.utils import thetacolors
from data import scrimdb


class Scrim(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    scrim_group = app_commands.Group(name="scrim", description="Create, view, or delete a scrim post.")

    @scrim_group.command(name="new", description="Create a new scrim")
    @app_commands.guild_only
    @app_commands.describe(team_name="What is the name of your team?")
    @app_commands.describe(results_or_division="How experienced is your team? Eg, LUTI Division 7, 4th place JR's Draft, etc.")
    @app_commands.describe(time_and_info="What time do you like to find a scrim for? Do you have a map list in mind?")
    @app_commands.describe(screen_ok="Does your team need to ban splattercolor screen?")
    @app_commands.choices(screen_ok=[
        discord.app_commands.Choice(name="Allow Screen", value=1),
        discord.app_commands.Choice(name="Disallow Screen", value=0)
    ])
    @app_commands.describe(post_where="Where would you like to send your post?")
    @app_commands.choices(post_where=[
        discord.app_commands.Choice(name="Globally (all servers)", value=1),
        discord.app_commands.Choice(name="In-House (just here)", value=0)
    ])
    async def scrim_new(self, interaction: discord.Interaction, team_name: str, results_or_division: str, time_and_map_list: str, screen_ok: discord.app_commands.Choice[int], post_where: discord.app_commands.Choice[int]):
        await interaction.response.send_message('ok (this is placeholder)')


async def setup(bot):
    await bot.add_cog(Scrim(bot))