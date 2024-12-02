import asyncio

import discord

from data import ServersDB, ScrimDB
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
    """Called from the postQueue / postUpdateStack system if the queue has less than 6 posts in it and the incoming post is not a duplicate."""
    postUpdateStack.insert(0, postObject)
    bot = postObject[1]
    servers = await ServersDB.get_global_channels()
    resolved_channels = []
    for server  in servers:
        resolved_channels.append(bot.get_channel(server.global_scrims_id))
    serversSplit = array_split(resolved_channels, 8)
    match postObject[3]:
        case 'create':
            await ScrimDB.garbage_disposal_for_scrim_messages(author_id=postObject[0])
            async with asyncio.TaskGroup() as task_group:
                for i in range(8):
                    completed = task_group.create_task(send_post(serversSplit[i], postObject[2], postObject[0]))
            postUpdateStack.pop(postObject)
        case 'update':
            pass
        case 'delete':
            client = postObject[1]
            scrimMessages = await ScrimDB.get_scrim_messages(postObject[0])
            scrimMessagesSplit = array_split(scrimMessages, 8)
            async with asyncio.TaskGroup() as task_group:
                for i in range(8):
                    task_group.create_task(delete_post(scrimMessagesSplit[i], postObject[1]))

async def process_post_queue() :
    """If the post queue has a post in it and the stack has less than 6 posts being processed,
    take the last post and process it UNLESS it is a duplicate of a post already being processed"""
    while True:
        while len(postQueue) > 0 and len(postUpdateStack) < 6:
            lastObject = postQueue[-1]
            if lastObject[0] in postUpdateStack:
                postQueue.insert(0, postQueue.pop(-1))
            else:
                await updatePost(postQueue.pop(-1))
        await asyncio.sleep(1)

async def send_post(discord_channels, embed, author_id,):
    post_message_ids = []
    channel_ids = []
    for channel in discord_channels:
        message: discord.Message =  await channel.send(embed=embed)
        post_message_ids.append(message.id)
        channel_ids.append(channel.id)
    await ScrimDB.add_scrim_messages(author_id, post_message_ids, channel_ids)

async def delete_post(messageObjects, client):
    for message in messageObjects:
        channel : discord.TextChannel = client.get_channel(message.channel_ID)
        await channel.delete_messages(message.message_ID)

