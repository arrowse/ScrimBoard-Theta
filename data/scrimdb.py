import logging

from data.prisma import db

class ScrimDB:
    def __init__(self, author_user_id):
        self.author_user_id = author_user_id

    @staticmethod
    async def check_scrim(author_id: int):
        scrim = await db.scrim.find_first(
            where={
                'uid': author_id,
            },
        )
        return scrim

    @staticmethod
    async def check_author(author_id: int):
        author = await db.postauthor.find_first(
            where={
                'uid': author_id,
            },
        ),
        teamname = await db.scrim.find_first(
            where={
                'uid': author_id,
            },
        )
        return author, teamname

    @staticmethod
    async def create_scrim(author_id: int, author_name: str, pfp, team_name, skill_level, info, screen_allowed, server_id):
        postauthor = await db.postauthor.upsert(
            where={
                'uid': author_id,
            },
            data= {
                'create': {
                    'uid': author_id,
                    'name': author_name,
                    'pfp': pfp,
                },
                'update': {
                    'name': author_name,
                    'pfp': pfp,
                }
        }
        )

        scrim = await db.scrim.upsert(
            where={
                'uid': author_id,
            },
            data={
                'create':{
                    'uid': author_id,
                    'teamname': team_name,
                    'skill_level': skill_level,
                    'info': info,
                    'screen_allowed': screen_allowed,
                    'server_id': server_id,
                },
                'update':{
                    'teamname': team_name,
                    'skill_level': skill_level,
                    'info': info,
                    'screen_allowed': screen_allowed,
                    'server_id': server_id,
                }
            }
        )
        return scrim

    @staticmethod
    async def add_scrim_messages(author_id: int, messageIDs: list):
        formattedMessageArray = []
        for messageID in messageIDs:
            dictObject = {'uid': author_id, 'messageID': messageID}
            formattedMessageArray.append(dictObject)
        await  db.messages.create_many(
            data=formattedMessageArray,
            skip_duplicates=True
        )
    # @staticmethod
    # async def accept_scrim():