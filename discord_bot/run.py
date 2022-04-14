import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import ASYNC_DATABASE_URI
from discord_bot.bot.commands import bot
from discord_bot.constants import DISCORD_ACCOUNT_TOKEN
from discord_bot.constants import DISCORD_LOG_FILENAME
from discord_bot.constants import LOGGING_LEVEL

# Define logging requirements
logging_level = logging.getLevelName(LOGGING_LEVEL)
logging.basicConfig(level=logging_level)
discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging_level)
handler = logging.FileHandler(filename=DISCORD_LOG_FILENAME, encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
discord_logger.addHandler(handler)

# Start db connection
if not ASYNC_DATABASE_URI:
    raise Exception("Cannot start without db connection")
engine = create_async_engine(ASYNC_DATABASE_URI, echo=True)
session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Start bot
bot.run(DISCORD_ACCOUNT_TOKEN)
