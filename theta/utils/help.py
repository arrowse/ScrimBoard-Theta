# Pulled from IPLSplatoon's radia repo: https://github.com/IPLSplatoon/Radia/blob/master/radia/utils/help.py
# MIT License
#
# Copyright (c) 2022 Xeift
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Contains HelpCommand class.

Stole and adapted from "https://github.com/offthedial/bot/blob/master/offthedialbot/help.py"
Thank me :)
- LeptoFlare
"""

from discord.ext import commands

from . import Embed


class HelpCommand(commands.DefaultHelpCommand):
    """Set up help command for the bot."""

    async def send_bot_help(self, mapping):
        """Send bot command page."""
        embed = self.create_embed(
            title=f"`{self.context.clean_prefix}help`",
            fields=[{
                "name": cog.qualified_name if cog else '\u200B',
                "value": "\n".join([
                    self.short(command)
                    for command in await self.filter_commands(cog_commands)
                ])} for cog, cog_commands in mapping.items() if await self.filter_commands(cog_commands)]
        )
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        """ Send cog command page.

        The most beautiful function I've ever written in python
        """
        embed = self.create_embed(
            title=cog.qualified_name.capitalize(),
            description=cog.description,
            **({"fields": [{
                "name": f"{cog.qualified_name.capitalize()} Commands:",
                "value": "\n".join([
                    self.short(command)
                    for command in cog.get_commands()])
            }]} if cog.get_commands() else {})
        )

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        """Send command group page."""
        embed = self.create_embed(
            title=self.short(group, False),
            description=group.help,
            **({"fields": [{
                "name": f"Subcommands:",
                "value": "\n".join([
                    self.short(command)
                    for command in await self.filter_commands(group.commands)
                ])
            }]} if await self.filter_commands(group.commands) else {})
        )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        """Send command page."""
        sig = self.get_command_signature(command)
        embed = self.create_embed(
            title=f"`{sig[:-1] if sig.endswith(' ') else sig}`",
            description=command.help,
        )
        await self.get_destination().send(embed=embed)

    def command_not_found(self, string):
        """Returns message when command is not found."""
        # noinspection PyTypeChecker
        return f"Command {self.short(string, False)} does not exist."

    def subcommand_not_found(self, command, string):
        """Returns message when subcommand is not found."""
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f"Command {self.short(command, False)} has no subcommand named `{string}`."
        else:
            return f"Command {self.short(command, False)} has no subcommands."

    async def send_error_message(self, error):
        """Send error message, override to support sending embeds."""
        await self.get_destination().send(embed=Embed(title="Command/Subcommand not found.", description=error))

    def create_embed(self, fields: list = (), **kwargs):
        """Create help embed."""
        embed = Embed(**kwargs)
        for field in fields:
            embed.add_field(**field, inline=False)
        embed.set_footer(
            text=f"Type {self.context.clean_prefix}help command for more info on a command. You can also type {self.context.clean_prefix}help category for more info on a category.")
        return embed

    def short(self, command, doc=True):
        """List the command as a one-liner."""
        return f'`{self.context.clean_prefix}{command}` {(command.short_doc if doc else "")}'