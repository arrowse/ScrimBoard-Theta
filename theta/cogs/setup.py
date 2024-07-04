import discord
import logging
from discord import app_commands
from discord.ext import commands
from typing import Literal

from theta.utils import thetacolors, ConfirmSetupDeletion
from data import ServersDB


async def send_already_configured(interaction: discord.Interaction, self, dbCheck):
    embed = discord.Embed(
        title=F"Setup found in {interaction.guild.name}",
        description="ScrimBoard is already configured in this server. Please use `/setup unlink-setup` to unlink the "
                    "current channels before setting up the server again.",
        color=thetacolors["error"]
    )
    if self and dbCheck:
        await attach_setup_channels_to_embed(self, embed, dbCheck)
    await interaction.edit_original_response(embed=embed)


async def send_already_configured_ctx(ctx, self, dbCheck):
    embed = discord.Embed(
        title=F"Setup found in {ctx.guild.name}",
        description="ScrimBoard is already configured in this server. Please use `/setup unlink-setup` to unlink the "
                    "current channels before setting up the server again.",
        color=thetacolors["error"]
    )
    if self and dbCheck:
        await attach_setup_channels_to_embed(self, embed, dbCheck)
    await ctx.send(embed=embed, ephemeral=True)


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
    category = dbCheck.category_id
    how_to_use_channel = self.bot.get_channel(dbCheck.how_to_use_id)
    local_scrims_channel = self.bot.get_channel(dbCheck.local_scrims_id)
    global_scrims_channel = self.bot.get_channel(dbCheck.global_scrims_id)
    logging.debug("Channels fetched, attaching setup channels to embed")
    if dbCheck.category_id is not None:
        embed.add_field(name="Category", value=F"{category}")
    if dbCheck.how_to_use_id is not None:
        embed.add_field(name="How to Use", value=F"{how_to_use_channel.mention}")
    if dbCheck.local_scrims_id is not None:
        embed.add_field(name="Local Scrims", value=F"{local_scrims_channel.mention}")
    if dbCheck.global_scrims_id is not None:
        embed.add_field(name="Global Scrims", value=F"{global_scrims_channel.mention}")


async def clear_channel_topics(self, dbCheck):
    how_to_use_channel = self.bot.get_channel(dbCheck.how_to_use_id)
    local_scrims_channel = self.bot.get_channel(dbCheck.local_scrims_id)
    global_scrims_channel = self.bot.get_channel(dbCheck.global_scrims_id)
    if dbCheck.how_to_use_id is not None:
        await how_to_use_channel.edit(topic="")
    if dbCheck.local_scrims_id is not None:
        await local_scrims_channel.edit(topic="")
    if dbCheck.global_scrims_id is not None:
        await global_scrims_channel.edit(topic="")



class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name='link')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def link(self, ctx):
        """Connect channels to ScrimBoard manually for more control over where posts are sent."""
        if ctx.invoked_subcommand is not None:
            return

        embed = discord.Embed(
            title="Link",
            description="Please run one of the following link commands to configure this channel:",
            color=thetacolors["default"]
        )
        embed.add_field(name="$link how-to", value="Sets this channel to receive ScrimBoard updates and guides.",
                        inline=False)
        embed.add_field(name="$link in-house",
                        value="Enables in-house scrims in your server and sets a channel to receive them.",
                        inline=False)
        embed.add_field(name="$link global",
                        value="Sets a channel to receive scrims created anywhere in the community. You can also do this with `/setup use-this-channel`",
                        inline=False)
        await ctx.send(embed=embed, ephemeral=True)

    @link.command(name='how-to')
    async def linkhowto(self, ctx):
        """Manually set a 'how_to' channel to receive ScrimBoard updates and guides."""
        await ServersDB.setuphowto(server_id=ctx.guild.id,
                                   server_name=ctx.guild.name,
                                   how_to_use=ctx.channel.id)
        await ctx.channel.edit(topic="ScrimBoard linked channel - How to Use")
        embed = discord.Embed(
            title="Channel linked",
            description=f"ScrimBoard updates and guides will be sent to this channel ({ctx.channel.mention}).",
            color=thetacolors["default"])
        await ctx.send(embed=embed)

    @link.command(name='in-house')
    async def linkinhouse(self, ctx):
        """Manually set an 'in_house' scrim channel to allow server members to host scrims only visible to other members."""
        result = await ServersDB.setupinhouse(server_id=ctx.guild.id,
                                              server_name=ctx.guild.name,
                                              local_scrims=ctx.channel.id)
        await ctx.channel.edit(topic="ScrimBoard linked channel - In-house")
        embed = discord.Embed(
            title="Channel linked",
            description=f"In-house scrims will be sent to this channel ({ctx.channel.mention}).",
            color=thetacolors["default"])
        await ctx.send(embed=embed)

    @link.command(name='global')
    async def linkglobal(self, ctx):
        """Manually set a 'global_scrims' channel to receive scrims from across the community. This is the same as
        /setup use-this-channel."""
        result = await ServersDB.setupminimal(server_id=ctx.guild.id,
                                              server_name=ctx.guild.name,
                                              global_scrims=ctx.channel.id)
        await ctx.channel.edit(topic="ScrimBoard linked channel - Global")
        embed = discord.Embed(
            title="Channel linked",
            description=f"Global scrims will now be sent to this channel ({ctx.channel.mention}).",
            color=thetacolors["default"])
        await ctx.send(embed=embed)

    @app_commands.command(name='setup', description='Setup ScrimBoard in your server!')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @app_commands.describe(options="Manage your server's ScrimBoard setup")
    @app_commands.choices(options=[
        discord.app_commands.Choice(name="use-this-channel (global scrims)", value="this"),
        discord.app_commands.Choice(name="create-new-channel (global scrims)", value="channel"),
        discord.app_commands.Choice(name="create-new-category (global & in-house scrims)", value="category"),
        discord.app_commands.Choice(name="check-current", value="check"),
        discord.app_commands.Choice(name="unlink-setup", value="delete")
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
                dbCheck = currentServerData
                # noinspection PyUnresolvedReferences
                if currentServerData is None:
                    await send_not_already_configured(interaction, prompt_to_setup=True)

                embed = discord.Embed(
                    title=F"Setup in {interaction.guild.name}",
                    description="Here are the channels configured for your server so far, if anything "
                                "looks off you can delete the setup with `/setup unlink-setup`.",
                    color=thetacolors["default"]
                )
                logging.debug(dbCheck)
                await attach_setup_channels_to_embed(self, embed, dbCheck)
                await interaction.edit_original_response(embed=embed)

            case 'delete':
                if currentServerData is None:
                    await send_not_already_configured(interaction, prompt_to_setup=True)
                    return
                await clear_channel_topics(self, currentServerData)
                await ServersDB.deletesetup(server_id=interaction.guild_id)
                embed = discord.Embed(
                    title=f"Setup unlinked in {interaction.guild.name}",
                    description="Scrims will no longer be sent to this server. You can relink previously "
                                f"connected channels; run `$help link` for more info.\nIf you wish to delete the related "
                                f"channels, it is now safe to do so.",
                    color=thetacolors["default"]
                )
                await interaction.edit_original_response(embed=embed)
            case 'channel':
                if currentServerData is not None:
                    await send_already_configured(interaction, self, dbCheck=currentServerData)
                    return

                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False,
                                                                                create_public_threads=False,
                                                                                create_private_threads=False,
                                                                                add_reactions=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                                      embed_links=True, attach_files=True,
                                                                      add_reactions=True)
                }
                logging.debug("trying to create a new channel")
                try:
                    global_scrims_channel = await interaction.guild.create_text_channel(name="global_scrims",
                                                                                        topic="ScrimBoard linked channel - Global",
                                                                                        overwrites=overwrites,
                                                                                        reason="ScrimBoard setup")
                    embed = discord.Embed(
                        title="Setup complete",
                        description=F"ScrimBoard configured successfully! Global scrims will now be sent to {global_scrims_channel.mention} as they are posted.",
                        color=thetacolors["default"]
                    )
                    logging.debug(f"Global scrims id is: {global_scrims_channel.id}")
                    result = await ServersDB.setupminimal(server_id=interaction.guild.id,
                                                          server_name=interaction.guild.name,
                                                          global_scrims=global_scrims_channel.id)
                    await interaction.edit_original_response(embed=embed)
                except discord.Forbidden:
                    embed = discord.Embed(
                        title="Setup failed",
                        description="ScrimBoard does not have permission to create channels in this server. Please make"
                                    " sure the 'manage-channels' permission is enabled.",
                        color=thetacolors["error"]
                    )
                    await interaction.edit_original_response(embed=embed)

            case 'category':
                if currentServerData is not None:
                    await send_already_configured(interaction, self, dbCheck=currentServerData)
                    return
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False,
                                                                                create_public_threads=False,
                                                                                create_private_threads=False,
                                                                                add_reactions=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                                      embed_links=True, attach_files=True,
                                                                      add_reactions=True)
                        }
                logging.debug("trying to create a new category")
                try:
                    category = await interaction.guild.create_category(name="ScrimBoard (Theta)", overwrites=overwrites)
                    how_to = await interaction.guild.create_text_channel(name="how-to-use", topic="ScrimBoard linked channel - Tutorial & Updates", overwrites=overwrites, category=category)
                    local_scrims = await interaction.guild.create_text_channel(name="in-house-scrims", topic="ScrimBoard linked channel - Local", overwrites=overwrites, category=category)
                    global_scrims = await interaction.guild.create_text_channel(name="global-scrims", topic="ScrimBoard linked channel - Global", overwrites=overwrites, category=category)
                    await ServersDB.setupall(server_id=interaction.guild.id, server_name=interaction.guild.name, category=category.id, how_to_use=how_to.id, local_scrims=local_scrims.id, global_scrims=global_scrims.id)
                except discord.Forbidden:
                    embed = discord.Embed(
                        title="Setup failed",
                        description="ScrimBoard does not have permission to create channels in this server. Please make"
                                    " sure the 'manage-channels' permission is enabled.",
                        color=thetacolors["error"]
                    )

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
                    await interaction.response.send_message(embed=embed, ephemeral=True)
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
