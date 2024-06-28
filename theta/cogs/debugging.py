"""Developer tools - Permissions are required to use these commands."""

import discord
from discord.ext import commands
import logging

from theta.utils import thetacolors
from theta.staticdata import isdeveloper


class Debugging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sync-all', description='Sync client tree to all servers')
    @commands.check(isdeveloper)
    async def syncall(self, ctx):
        """Sync slash commands to all servers (requires developer permissions)"""
        embed = discord.Embed(
            title="Sync-all",
            description="Syncing command tree to all servers...",
            color=thetacolors["waiting"]
        )
        syncAllReply = await ctx.send(embed=embed)
        try:
            syncedCommands = await self.bot.tree.sync()
            embed = discord.Embed(
                title="Sync-all",
                description=f"Synced {len(syncedCommands)} commands to all servers.",
                color=thetacolors["default"]
            )
            await syncAllReply.edit(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Sync-all",
                description="An error occurred while syncing the command tree to all servers, please check the "
                            "console for details.",
                color=0xae8e8e
            )
            logging.error(f"An error occurred while syncing the command tree to all servers: {e}")
            await syncAllReply.edit(embed=embed)

    @commands.command(name='sync-here', description='Sync client tree to current server')
    @commands.check(isdeveloper)
    async def synchere(self, ctx):
        """Sync slash commands to current server (requires developer permissions)"""
        embed = discord.Embed(
            title="Sync-here",
            description=F"Syncing command tree to {ctx.guild.name}...",
            color=thetacolors["waiting"]
        )
        syncHereReply = await ctx.send(embed=embed)
        try:
            syncedCommands = await self.bot.tree.sync(guild=ctx.guild)
            embed = discord.Embed(
                title="Sync-here",
                description=f"Synced {len(syncedCommands)} commands to {ctx.guild.name}.",
                color=thetacolors["default"]
            )
            await syncHereReply.edit(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Sync-here",
                description="An error occurred while syncing the command tree to this server, please check the "
                            "console for details.",
                color=0xae8e8e
            )
            logging.error(f"An error occurred while syncing the command tree to this server: {e}")
            await syncHereReply.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(Debugging(bot))
