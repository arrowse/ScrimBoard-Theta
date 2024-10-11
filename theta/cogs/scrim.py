from pydoc import describe

import discord
from discord import app_commands
from discord.ext import commands

from theta.utils import thetacolors
from data .scrimdb  import ScrimDB
from theta.staticdata import isBanned
from theta.utils import Embed

async def send_scrim_embed(interaction: discord.Interaction):
    embed = discord.Embed(
        title=F"New Scrim",
        description=F"Fetching scrim data for your account ({interaction.user.name})",
        color=thetacolors["waiting"]
    )
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embed, ephemeral=True)
    return embed

async def send_scrim_found(interaction: discord.Interaction):
    embed = discord.Embed(
        title=F"New Scrim",
        description="You already have an active scrim! ",
        color=thetacolors["error"]
    )
    await interaction.edit_original_response(embed=embed)
async def send_scrim_not_found(interaction: discord.Interaction):
    embed = discord.Embed(
        title=F"Scrim not found",
        description="An active scrim could not be found for your account",
        color=thetacolors["error"]
    )
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embed, ephemeral=True)


class Scrim(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    scrim_group = app_commands.Group(name="scrim", description="Create, view, or delete a scrim post.")

    @scrim_group.command(name="view", description="Check and manage a current scrim.")
    async def scrim_view(self, interaction: discord.Interaction):
        postAuthor = await ScrimDB.check_author(interaction.user.id)
        if not await ScrimDB.check_scrim(interaction.user.id):
            embed = discord.Embed(title='Scrim View')
            interaction.response.send_message(embed=embed, ephemeral=True)
            await send_scrim_not_found(interaction)
            return
        embed= discord.Embed(
            title=f"{postAuthor.name} is looking for a scrim in {interaction.guild.name}" if interaction.guild else f"{postAuthor.name} is looking for a scrim!",
            color=thetacolors['default']
        )
        await Embed.attach_scrim_details(interaction, embed)
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
    async def scrim_new(self, interaction: discord.Interaction, team_name: str, results_or_division: str, time_and_info: str, screen_ok: discord.app_commands.Choice[int], post_where: discord.app_commands.Choice[int]):
        embed = await send_scrim_embed(interaction)
        if await isBanned(interaction.user.id):
            await Embed.return_active_ban_found(interaction)
            return
        if await ScrimDB.check_scrim(interaction.user.id):
            await send_scrim_found(interaction)
            return
        if interaction.guild.id:
            server_ID = interaction.guild.id
        else:
            server_ID = 'NULL'
        embed= discord.Embed(
            title=f"{team_name} is looking for a scrim in {interaction.guild.name}" if interaction.guild else f"{team_name} is looking for a scrim!",
            color=thetacolors['default']
        )
        await ScrimDB.create_scrim(interaction.user.id, interaction.user.name, interaction.user.avatar.url, team_name, results_or_division, time_and_info, bool(screen_ok.value), server_ID)
        await Embed.attach_scrim_details(interaction, embed)
        # if post_where.value == 1:
        #     embed.description=f"Your scrim is being sent to **all servers.** This message will update once the post is done being shared."
        # else:
        #     embed.description=f"Your scrim has been sent to this server's in-house scrim channel."
        await interaction.edit_original_response(embed=embed)



async def setup(bot):
    await bot.add_cog(Scrim(bot))
