import os
from copy import copy

from furl import furl

from typeshed import ConfigDict
from typeshed import DBConfigDict
from typeshed import DiscordConfigDict

DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

database_furl = furl(
    scheme="postgresql",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host="localhost",
    path=DATABASE_NAME,
)

DATABASE_URI = copy(database_furl.url)

database_furl.set(scheme="postgresql+asyncpg")
ASYNC_DATABASE_URI = database_furl.url

DISCORD_ACCOUNT_TOKEN = os.environ.get("DISCORD_ACCOUNT_TOKEN", "token")

DISCORD_LOG_FILENAME = "logs/discord.log"

config_dict = ConfigDict(
    db=DBConfigDict(database_uri=DATABASE_URI, async_database_uri=ASYNC_DATABASE_URI),
    discord=DiscordConfigDict(
        account_token=DISCORD_ACCOUNT_TOKEN,
        log_filename=DISCORD_LOG_FILENAME,
        log_level="DEBUG",
    ),
)
