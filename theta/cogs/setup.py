import discord
import logging
from discord import app_commands
from discord.ext import commands

from theta.utils import thetacolors
from data import ServersDB


async def send_already_configured(interaction: discord.Interaction, self, dbCheck):
    embed = discord.Embed(
        title=F"Setup found in {interaction.guild.name}",
        description="ScrimBoard is already configured in this server. Please use `/setup delete-setup` to unlink the current channels before setting up the server again.",
        color=thetacolors["error"]
    )
    if self and dbCheck:
        await attach_setup_channels_to_embed(self, embed, dbCheck)
    await interaction.edit_original_response(embed=embed)


async def send_not_already_configured(interaction: discord.Interaction, prompt_to_setup: bool):
    notconfiguredembed = discord.Embed(
        title=F"Setup not found in {interaction.guild.name}",
        description=F"ScrimBoard hasn't been configured for this server yet. {'Run `/setup` to get started!' if prompt_to_setup else ''}",
        color=thetacolors["default"] if not prompt_to_setup else thetacolors["error"]
    )
    # noinspection PyUnresolvedReferences
    await interaction.edit_original_response(embed=notconfiguredembed)


async def send_cannot_send_messages(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Setup this channel",
        description="ScrimBoard does not have permission to send messages in this channel. "
                    "Please make sure the 'view-channel', and 'send-messages' permissions are enabled.",
        color=thetacolors["error"]
    )
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embed, ephemeral=True)


async def send_setup_embed(interaction: discord.Interaction, where: str):
    embed = discord.Embed(
        title=F"Setup",
        description=F"Fetching ScrimBoard data for this server and {where} ...",
        color=thetacolors["waiting"]
    )
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embed)


async def attach_setup_channels_to_embed(self, embed: discord.Embed, dbCheck):
    category_channel = dbCheck.category_id
    how_to_use_channel = self.bot.get_channel(dbCheck.how_to_use_id)
    local_scrims_channel = self.bot.get_channel(dbCheck.local_scrims_id)
    global_scrims_channel = self.bot.get_channel(dbCheck.global_scrims_id)
    if dbCheck.category_id is not None:
        embed.add_field(name="Category", value=F"{category_channel}")
    if dbCheck.how_to_use_id is not None:
        embed.add_field(name="How to Use", value=F"{how_to_use_channel.mention}")
    if dbCheck.local_scrims_id is not None:
        embed.add_field(name="Local Scrims", value=F"{local_scrims_channel.mention}")
    if dbCheck.global_scrims_id is not None:
        embed.add_field(name="Global Scrims", value=F"{global_scrims_channel.mention}")


class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='setup', description='Setup ScrimBoard in your server!' )
    @commands.has_permissions(administrator=True)
    @app_commands.guild_only
    @app_commands.describe(options="Manage your server's ScrimBoard setup")
    @app_commands.choices(options=[
        discord.app_commands.Choice(name="setup-this-channel", value="this"),
        discord.app_commands.Choice(name="setup-new-channel (minimal setup)", value="channel"),
        discord.app_commands.Choice(name="setup-new-category (complete setup)", value="category"),
        discord.app_commands.Choice(name="check-current-setup", value="check"),
        discord.app_commands.Choice(name="delete-setup", value="delete")
    ])
    async def configure(self, interaction: discord.Interaction, options: discord.app_commands.Choice[str]):
        """Setup ScrimBoard in your server, check the status of your current setup, or delete it."""

        logging.debug(F"Choice: {options.value}")
        logging.debug(F"Checking setup for {interaction.guild.name}...")
        currentServerData = await ServersDB.check_server_setup(server_id=interaction.guild_id)
        try:
            logging.debug("Trying to send embed")
            await send_setup_embed(interaction, interaction.channel.mention)
        except discord.Forbidden:
            await send_cannot_send_messages(interaction)
            return

        match options.value:
            case 'check':
                dbCheck = await ServersDB.check_server_setup(server_id=interaction.guild_id)
                # noinspection PyUnresolvedReferences
                if dbCheck is None:
                    await send_not_already_configured(interaction, prompt_to_setup=True)

                embed = discord.Embed(
                    title=F"Setup in {interaction.guild.name}",
                    description="Here are the channels configured for your server so far, if anything "
                                "looks off you can delete the setup with `/setup delete-setup`.",
                    color=thetacolors["default"]
                )
                logging.debug(dbCheck)
                logging.debug(dbCheck.how_to_use_id)
                await attach_setup_channels_to_embed(self, embed, dbCheck)
                await interaction.edit_original_response(embed=embed)

            case 'delete':
                return
            case 'channel':
                return
            case 'category':
                return
            case 'this':
                if currentServerData is not None:
                    # noinspection PyUnresolvedReferences
                    await send_already_configured(interaction, self, dbCheck=currentServerData)
                    return

                logging.debug(F"Setting up ScrimBoard in {interaction.channel.mention} ({interaction.channel.name})...")
                result = await ServersDB.setupminimal(server_id=interaction.guild.id,
                                                      server_name=interaction.guild.name,
                                                      global_scrims=interaction.channel.id)

                logging.debug("DB Passed back to setup.py")
                if result is None:
                    embed = discord.Embed(
                        title="Setup failed",
                        description="An unexpected error occurred while configuring this channel.",
                        color=thetacolors["error"]
                    )
                    await interaction.edit_original_response(embed=embed)
                    return

                embedSuccess = discord.Embed(
                    title="Setup complete",
                    description=F"ScrimBoard configured successfully! Global scrims will now be sent to this channel "
                                F"({interaction.channel.mention}) as they are created.",
                    color=thetacolors["default"]
                )
                logging.debug("sending final reply")
                try:
                    await interaction.channel.edit(topic="ScrimBoard linked channel - Global")
                except discord.Forbidden:
                    logging.debug(("No permission to edit channel description, oh well"))
                await interaction.edit_original_response(embed=embedSuccess)

    @configure.error
    async def configure_error(self, interaction):
        embed = discord.Embed(
            title="Setup Error",
            description="'Administrator' is required to manage the ScrimBoard setup for this server. Please check "
                        "your permissions and try again, or contact an admin for this server.",
            color=thetacolors["error"]
        )
        await interaction.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Setup(bot))
