# Pulled from IPLSplatoon's radia repo: https://github.com/IPLSplatoon/Radia/blob/master/radia/bot.py
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

import logging

import discord
from discord.ext import commands

from theta import utils


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_command = utils.HelpCommand()

    async def setup_hook(self) -> None:
        pass

    async def on_ready(self):
        logging.info("Logged in as: %s", self.user.name)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=utils.Embed(
                title="Error: **Missing Required Argument**",
                description=f"You can use `{ctx.prefix}help` for help."))
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send(embed=utils.Embed(
                title="Error: **Missing Permissions**",
                description=f"This is probably a mistake, please notify staff about this."))
        elif isinstance(error, (commands.CommandNotFound, commands.MissingRole)):
            return
        else:
            logging.error(error)
            raise error
