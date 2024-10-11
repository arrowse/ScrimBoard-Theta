import discord
from discord import app_commands
from discord.ext import commands

from data.scrimdb import ScrimDB
from theta.utils import thetacolors
from theta.staticdata import isdeveloper, ispartner, dmcheck, isScrimBoardBanned


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='ping', description='Latency test')
    async def ping(self, ctx):
        """Get the latency of the bot in milliseconds."""
        embed = discord.Embed(title=" Pong!",
                              description=f"Latency: `{round(self.bot.latency * 1000)}ms`",
                              color=thetacolors["default"])
        await ctx.send(embed=embed)

    @app_commands.command(name='whoami', description='Retrieve everything ScrimBoard knows about you')
    async def whoami(self, interaction: discord.Interaction):
        """Get everything ScrimBoard knows about you."""
        embed = discord.Embed(title="Whoami?",
                              description="Retrieving your related data, please wait.",
                              color=thetacolors["waiting"])
        await interaction.response.send_message(embed=embed, ephemeral=True)
        ctx = await self.bot.get_context(interaction)

        partner = await ispartner(ctx)
        developer = await isdeveloper(ctx)
        dmsopen = await dmcheck(interaction.user)
        banned =  await isScrimBoardBanned(interaction.user.id)
        restricted = False
        activepost = ScrimDB.check_scrim(interaction.user.id)

        if not dmsopen or banned:
            restricted = True

        embed = discord.Embed(title=F"{interaction.user.display_name} ({interaction.user.name})",
                              description=F" User ID: `{interaction.user.id}`,  {'DMs Open: True' if dmsopen else ' '} ",
                              color=thetacolors["default"])
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.add_field(name="Permissions:",
                        value=f"{'Developer (root access)' if developer else 'Partner (moderation access)' if partner else 'Restricted (no-post interactions)' if restricted else 'User'}")

        embed.add_field(name="Scrim Post:",
                        value=F"{'Not looking for a scrim.' if not activepost else 'Active scrim found.'}")
        await interaction.edit_original_response(embed=embed)
        if not dmsopen:
            embed.add_field(name="DMs closed", value="In order to accept or create scrims, you'll need to allow DMs "
                                                     "from any server ScrimBoard is in to receive updates.",)
        if banned:
            embed.add_field(name="Active ban found", value="You have been an active ScrimBoard ban preventing you "
                                                           "from creating and accepting scrims.")


async def setup(bot):
    await bot.add_cog(Misc(bot))
