import logging
from data.prisma import db

class ScrimDB:
    def __init__(self, author_user_id):
        self.author_user_id = author_user_id

    @staticmethod
    async def check_scrim(author_id: int):
        scrim = await db.scrim.find_first(
            where={
                'uid': author_id
            },
            select={
                'scrims': True
            }
        )
        return scrim

    @staticmethod
    async def create_scrim(author_id: int, author_name: str, pfp, team_name, skill_level, info, screen_allowed, server_id):
        scrim = await db.postauthor.upsert(
            where={
                uid: author_id,
            },
            data={
                uid: author_id,
                name: author_name,
                pfp: pfp,
                scrims: {
                    teamname: team_name,
                    skill_level: skill_level,
                    info: info,
                    screen_allowed: screen_allowed,
                    server_id: server_id,
                }
            }
        )
        return scrim

    # Parse an array of the message ids under data using upsert to update the data.
    # Because the author entry already exists, we don't *need* to use create many.
    # @staticmethod
    # async def add_scrim_messages(author_id: int, messageIDs: array):
    #     scrimmessageids = await db.postauthor.createMany(
    #         data =
    #     )

    # @staticmethod
    # async def accept_scrim():