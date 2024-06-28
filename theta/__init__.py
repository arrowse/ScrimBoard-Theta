# Pulled from IPLSplatoon's radia repo: https://github.com/IPLSplatoon/Radia/blob/master
# Initiate logging

import os
import logging

debug = os.getenv("DEBUG", "false").lower() != "false"

# Initialize logging
logging.basicConfig(
    level=(logging.DEBUG if debug else logging.INFO),
    format="\033[31m%(levelname)s\033[0m \033[90min\033[0m \033[33m%(filename)s\033[0m \033[90mon\033[0m %(asctime)s\033[90m:\033[0m %(message)s",
    datefmt="\033[32m%m/%d/%Y\033[0m \033[90mat\033[0m \033[32m%H:%M:%S\033[0m",
)
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.WARNING)

logging.getLogger(__name__)

if debug:
    logging.info(
        ".env - 'DEBUG' key found. Running in debug mode, do not use in production."
    )
