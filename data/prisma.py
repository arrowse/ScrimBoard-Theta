from prisma import Prisma

db = Prisma(auto_register=True)


async def runQueryEngine():
    await db.connect()
