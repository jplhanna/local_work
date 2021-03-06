from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from discord.ext.commands import Context

from src.bot.constants import ALREADY_REGISTERED_MESSAGE
from src.bot.constants import NEW_USER_MESSAGE
from src.bot.constants import REGISTER_FIRST_MESSAGE
from src.containers import Container
from src.exceptions import NoIDProvided
from src.services import QuestService
from src.services import UserService


@inject
async def check_and_register_user(ctx: Context, user_service: UserService = Provide[Container.user_service]) -> str:
    discord_id = ctx.author.id
    if not discord_id:
        raise NoIDProvided()
    if await user_service.get_user_by_discord_id(discord_id):
        return ALREADY_REGISTERED_MESSAGE
    await user_service.create_user(discord_id=discord_id)
    return NEW_USER_MESSAGE


@inject
async def add_quest_to_user(
    ctx: Context,
    quest_name: str,
    quest_service: QuestService = Provide[Container.quest_service],
    user_service: UserService = Provide[Container.user_service],
) -> str:
    user = await user_service.get_user_by_discord_id(ctx.author.id)
    if not user:
        return REGISTER_FIRST_MESSAGE
    res = await quest_service.accept_quest_if_available(user, quest_name)
    return res
