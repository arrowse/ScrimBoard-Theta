import logging
from builtins import int
from typing import List, Any
import logging
from data.prisma import db


class ServersDB:
    def __int__(self, server_id, server_name, category_id, how_to_use_id, local_scrims_id, global_scrims_id):
        self.server = server_id
        self.servername = server_name
        self.category = category_id
        self.how_to_use = how_to_use_id
        self.local_scrims = local_scrims_id
        self.global_scrims = global_scrims_id

    @staticmethod
    async def check_server_setup(server_id: int):
        server = await db.server.find_first(
            where={
                "dserver_id": server_id
            }
        )
        logging.debug(f"Server check response: {server}")
        return server

    @staticmethod
    async def setupminimal(server_id: int, server_name: str, global_scrims: int) -> object:
        try:
            server = await db.server.upsert(
                where={
                    "dserver_id": server_id
                },
                data={
                    'create': {
                        "dserver_id": server_id,
                        "name": server_name,
                        "global_scrims_id": global_scrims
                    },
                    'update': {
                        "global_scrims_id": global_scrims
                    }
                })
            logging.debug(f"Minimal server setup response: {server}")
            return "Success"
        except Exception as e:
            logging.error(f"Error setting up minimal server: {e}")
        return None

    @staticmethod
    async def setupall(server_id: int, server_name: str, category: int, how_to_use: int, local_scrims: int, global_scrims: int):
        try:
            server = await db.server.upsert(
                where={
                    "dserver_id": server_id
                },
                data={
                    'create': {
                        'dserver_id': server_id,
                        'name': server_name,
                        'category_id': category,
                        'how_to_use_id': how_to_use,
                        'local_scrims_id': local_scrims,
                        'global_scrims_id': global_scrims
                    },
                    'update': {
                        'category_id': category,
                        'how_to_use_id': how_to_use,
                        'local_scrims_id': local_scrims,
                        'global_scrims_id': global_scrims
                    }
                }
            )
        except Exception as e:
            logging.error(f"failed to configure category {e}")

    @staticmethod
    async def setuphowto(server_id: int, server_name: str, how_to_use: int) -> object:
        try:
            server = await db.server.upsert(
                where={
                    "dserver_id": server_id
                },
                data={
                    'create': {
                        "dserver_id": server_id,
                        "name": server_name,
                        "how_to_use_id": how_to_use
                    },
                    'update': {
                        "how_to_use_id": how_to_use
                    }
                })
            logging.debug(f"how-to setup response: {server}")
            return "Success"
        except Exception as e:
            logging.error(f"Error setting up how-to: {e}")
        return None

    @staticmethod
    async def setupinhouse(server_id: int, server_name: str, local_scrims: int) -> object:
        try:
            server = await db.server.upsert(
                where={
                    "dserver_id": server_id
                },
                data={
                    'create': {
                        "dserver_id": server_id,
                        "name": server_name,
                        "local_scrims_id": local_scrims
                    },
                    'update': {
                        "local_scrims_id": local_scrims
                    }
                })
            logging.debug(f"Minimal server setup response: {server}")
            return "Success"
        except Exception as e:
            logging.error(f"Error setting up in-house: {e}")
        return None

    @staticmethod
    async def deletesetup(server_id: int):
        try:
            deleted = await db.server.delete(
                where={
                    "dserver_id": server_id
                },
            )
            return deleted
        except Exception as e:
            logging.error(f"Error deleting server data: {e}")
        return None
