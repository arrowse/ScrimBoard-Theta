# Pulled from IPLSplatoon's radia repo: https://github.com/IPLSplatoon/Radia/blob/master/radia/utils/embed.py
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

"""Utilities to help with embedding."""

from datetime import datetime

from .colors import thetacolors
from data.scrimdb import ScrimDB

import discord

class Embed(discord.Embed):
    """A custom embed object."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, color=0x9492BA, **kwargs)
        self.set_footer(text="Theta", icon_url="https://cdn.discordapp.com/avatars/1256127837799317504/5e6684da64a98d38cadbee398f2a9469?size=1024")
        self.timestamp = datetime.now(
        )

    @staticmethod
    def list(items: list, *, ordered=False) -> str:
        """ Return a formatted list

        :param list items: List of items to format
        :param bool ordered: Whether the list should be ordered or not
        :return str:
            The list codeblock
        """
        def format(i, item):
            """Format a list item."""
            if ordered:
                return f"> `{i}.` {item}"
            else:
                return f"> `-` {item}"

        return "\n".join([
            *[format(i, item) for i, item in enumerate(items)],
        ])

    @staticmethod
    def file_list(items: list, *, ordered=False) -> str:
        """ Return a formatted list

        :param list items: List of items to format
        :param bool ordered: Whether the list should be ordered or not
        :return str:
            The list codeblock
        """

        def format(i, item):
            """Format a list item."""
            if ordered:
                return f"- {i}. {item}"
            else:
                return f"- {item}"

        return "\n".join([
            *[format(i, item) for i, item in enumerate(items)],
        ])

    @staticmethod
    def emoji_bool(value: bool) -> str:
        """Return an emoji based the Boolean value to display to the user instead of boring text."""
        return {
            True: "\u2705",
            False: "\u274c"
        }[value]

    @staticmethod
    async def return_active_ban_found(interaction: discord.Interaction):
        embed = discord.Embed(
            title=F"No Permission",
            description="Your account is currently banned from creating or accepting scrims.",
            color=thetacolors["error"]
        )
        await interaction.edit_original_response(embed=embed)

    @staticmethod
    async def attach_scrim_details(interaction: discord.Interaction, embed: discord.Embed):
        scrimDetails = await ScrimDB.check_scrim(interaction.user.id)
        if scrimDetails:
            embed.set_author(name=f"Posted by {interaction.user.name}", icon_url=interaction.user.avatar.url),
            embed.add_field(name="Time and info", value=f"{scrimDetails.info}", inline=False)
            embed.add_field(name="Prior results", value=f"{scrimDetails.skill_level}")
            embed.add_field(name="Screen Allowed?", value=f"{scrimDetails.screen_allowed}")
            if scrimDetails.accepter_name:
                embed.add_field(name="Accepted by",value=f"{scrimDetails.accepter_name} (UID {scrimDetails.accepter_uid})", inline=False)