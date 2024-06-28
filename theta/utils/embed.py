# Pulled from IPLSplatoon's radia repo: https://github.com/IPLSplatoon/Radia/blob/master/radia/utils/embed.py

"""Utilities to help with embedding."""

from datetime import datetime
from typing import List

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