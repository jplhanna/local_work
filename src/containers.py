from asyncio import current_task
from contextlib import asynccontextmanager
from logging import FileHandler
from logging import Formatter
from logging import getLogger
from typing import AsyncGenerator
from typing import List

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration
from dependency_injector.providers import Factory
from dependency_injector.providers import Resource
from dependency_injector.providers import Singleton
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import config_dict
from src.helpers.sqlalchemy_helpers import BaseModel
from src.models import Quest
from src.models import User
from src.repositories import BaseRepository
from src.services import QuestService
from src.services import UserService

logger = getLogger(__name__)

WIRE_TO: List[str] = []


class Database:
    def __init__(self, db_url: str) -> None:
        self._async_engine = create_async_engine(db_url, echo=True)
        self._session_factory = async_scoped_session(
            sessionmaker(
                self._async_engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )

    async def create_database(self) -> None:
        current_session = self.get_session()
        await current_session.run_sync(BaseModel.metadata.create_all)

    def get_session(self) -> AsyncSession:
        return self._session_factory()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()


class DiscordLogger:
    def __init__(self, logging_level: str, file_name: str) -> None:
        self.discord_logger = getLogger("discord")
        self.discord_logger.setLevel(logging_level)
        self.handler = FileHandler(filename=file_name, encoding="utf-8", mode="w")
        self.handler.setFormatter(Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
        self.discord_logger.addHandler(self.handler)


class Container(DeclarativeContainer):
    config = Configuration("configuration")
    config.from_dict(config_dict)  # type: ignore[arg-type] # The type is correct
    discord_logging = Resource(DiscordLogger)
    discord_logging.add_kwargs(logging_level=config.discord.log_level, file_name=config.discord.log_filename)

    db_client = Singleton(Database, db_url=config.db.async_database_uri)

    user_repository = Factory(BaseRepository, session_factory=db_client.provided.get_session, model=User)
    user_service = Factory(UserService, repository=user_repository)

    quest_repository = Factory(BaseRepository, session_factory=db_client.provided.get_session, model=Quest)
    quest_service = Factory(QuestService, repository=quest_repository)
