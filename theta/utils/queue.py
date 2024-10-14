import asyncio

import discord

from data import ServersDB
from numpy import array_split

# Posts waiting to be updated
postQueue = []
# Posts currently being updated
postUpdateStack = []

# POST OBJECT ARRAY
# [0] - User ID
# [1] - Self.bot (client)
# [2] - Embed
# [3] - Action ['create' OR 'update' OR 'delete']

async def updatePost(postObject):
    """Called from the postQueue / postUpdateStack system if the queue has less than 6 posts in it and the incoming post is not a duplicate. See more in utils/queue.py."""
    postUpdateStack.insert(0, postObject)
    bot = postObject[1]
    servers = await ServersDB.get_global_channels()
    resolved_channels = []
    for server  in servers:
        resolved_channels.append(bot.get_channel(server.global_scrims_id))
    serversSplit = array_split(resolved_channels, 8)
    post_message_ids = []
    match postObject[3]:
        case 'create':
            async with asyncio.TaskGroup() as task_group:
                for i in range(0,8):
                    updateStack= task_group.create_task(send_post(serversSplit[i], postObject[2]))
        case 'update':
            pass
        case 'delete':
            pass



async def process_post_queue() :
    """If the post queue has a post in it and the stack has less than 6 posts being processed,
    take the last post and process it UNLESS it is a duplicate of a post already being processed"""
    while True:
        while len(postQueue) > 0 and len(postUpdateStack) < 6:
            if postQueue[-1] in postUpdateStack:
                postQueue.insert(0, postQueue.pop(-1))
            await updatePost(postQueue.pop(-1))
        await asyncio.sleep(1)

async def send_post(discord_channel: discord.channel, embed):
    for channel in discord_channel:
        await channel.send(embed=embed)