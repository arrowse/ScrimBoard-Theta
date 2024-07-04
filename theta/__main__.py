# Pulled from IPLSplatoon's radia repo: https://github.com/IPLSplatoon/Radia/blob/master
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
Initializes the bot

This includes importing the bot, loading the cogs, setting the prefix, etc.
"""

import os
import logging
import asyncio

from discord import Intents
from discord.ext import commands

from theta import cogs
from theta.bot import Bot
from data.prisma import runQueryEngine

# Create Bot
intents = Intents.all()
# intents.members = True
debug = os.getenv("DEBUG", "false").lower() != "false"
bot = Bot(commands.when_mentioned_or('$') if not debug else "!", intents=intents)


# Get token from env variables
if not (token := os.getenv("TOKEN")):
    logging.error(".env - 'TOKEN' key not found. Cannot start bot.")
    raise EnvironmentError


async def run_bot() -> None:
    """
    Loads in cogs and starts bot
    :return: None
    """
    await runQueryEngine()
    async with bot:
        for cog in cogs.names:
            try:
                await bot.load_extension("theta.cogs." + cog)
                logging.debug("Loaded cogs.%s", cog)
            except Exception as e:
                logging.warning("Failed to load cogs.%s", cog)
                logging.error(type(e).__name__, e)
        await bot.start(token)

asyncio.run(run_bot())
