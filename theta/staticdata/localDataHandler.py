import json
import discord

async def isdeveloper(ctx) -> bool:
    with open("theta/staticdata/trusted.json", "r") as trusted:
        permissionsList = json.load(trusted)
        if ctx.author.id in permissionsList["developer"]:
            trusted.close()
            return True
        trusted.close()
        return False


async def ispartner(ctx) -> bool:
    with open("theta/staticdata/trusted.json", "r") as trusted:
        permissionsList = json.load(trusted)
        if ctx.author.id in permissionsList["developer"]:
            trusted.close()
            return True
        if ctx.author.id in permissionsList["partner"]:
            trusted.close()
            return True
        trusted.close()
        return False


async def dmcheck(user: discord.User) -> bool:
    try:
        await user.send()
    except discord.Forbidden:
        return False
    except discord.HTTPException:
        return True
