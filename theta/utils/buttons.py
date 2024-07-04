import discord
from data import ServersDB
from theta.utils import thetacolors


class ConfirmSetupDeletion(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @discord.ui.button(label="Unlink", style=discord.ButtonStyle.gray)
    async def unlink(self, interaction: discord.Interaction, button: discord.Button):
        button.label = "Unlinking..."
        deleted = await ServersDB.deletesetup(server_id=interaction.guild.id)
        embed = discord.Embed(
            title=f"Setup unlinked in {interaction.message.guild.name}",
            description="Scrims will no longer be sent to this server. You can relink previously connected channels "
                        "with `$link <type>`. For more info, run `$help link`.",
            color=thetacolors["default"]
        )
        await interaction.response.send_message(embed=embed, view=None, ephemeral=False)
        return

    @discord.ui.button(label="Unlink & Delete", style=discord.ButtonStyle.danger)
    async def unlinkanddelete(self, interaction: discord.Interaction, button: discord.Button):
        button.label = "Unlinking..."
        currentServerData = await ServersDB.check_server_setup(server_id=interaction.guild.id)
        category_channel = currentServerData.category_id
        how_to_use_channel = self.bot.get_channel(currentServerData.how_to_use_id)
        local_scrims_channel = self.bot.get_channel(currentServerData.local_scrims_id)
        global_scrims_channel = self.bot.get_channel(currentServerData.global_scrims_id)
        if currentServerData.global_scrims_id is not None:
            await global_scrims_channel.delete()
        if currentServerData.local_scrims_id is not None:
            await local_scrims_channel.delete()
        if currentServerData.how_to_use_id is not None:
            await how_to_use_channel.delete()
        if currentServerData.category_id is not None:
            await category_channel.delete()
        await ServersDB.deletesetup(server_id=interaction.message.guild.id)
        embed = discord.Embed(
            title=f"Setup unlinked and deleted in {interaction.guild.name}",
            description="Scrim channels have been unlinked and deleted, if you wish to reconfigure ScrimBoard again you"
                        "can do so anytime with `/setup`.",
            color=thetacolors["default"])
        if interaction.channel is None:
            await interaction.user.send(embed=embed)
        else:
            await interaction.response.send_message(embed=embed, view=None, ephemeral=False)