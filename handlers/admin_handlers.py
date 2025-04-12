from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
from secret import ADMIN_IDS, BOT_ID
from databases.database import add_client, sql_changes, sql_request
from services.service import history_dict, History
from aiogram.exceptions import AiogramError
import logging

router: Router = Router()
router.message.filter(F.from_user.id.in_(ADMIN_IDS))


logger = logging.getLogger(__name__)


@router.message(F.text.startswith("/code "))
async def code_complete(message: Message):
    try:
        result_code = "return 0"
        try:
            exec(message.text[6:])
        except Exception as err:
            result_code = err
        await message.answer(text=str(result_code))
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.message(F.text.startswith("/get_log"))
async def get_log(message: Message):
    try:
        await message.answer_document(FSInputFile("log.log"))
    except Exception as err:
        await message.answer("Не получается отправить")
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.message(F.text.startswith("/add "))
async def add_clients(message: Message, bot: Bot):
    try:
        if len(message.text.split()[1:]) == 2:
            group_id, channel_id = map(int, message.text.split()[1:])
            try:
                result1 = await bot.get_chat_member(group_id, BOT_ID)
                result2 = await bot.get_chat_member(channel_id, BOT_ID)
                if not (
                    result1.status == "administrator" and result1.can_delete_messages
                ):
                    raise AiogramError("Не выданы права в группе")
                if not (
                    result2.status == "administrator"
                    and result2.can_delete_messages
                    and result2.can_post_messages
                    and result2.can_edit_messages
                ):
                    raise AiogramError("Не выданы права в канале")
            except AiogramError as err:
                await message.answer(str(err))
                await message.answer(
                    result1.model_dump_json(indent=2, exclude_none=True)
                )
                await message.answer(
                    result2.model_dump_json(indent=2, exclude_none=True)
                )
            else:
                add_client(group_id, channel_id)
                history_dict[group_id] = History(channel_id)
                await message.answer(
                    f"group_id: '{group_id}', channel_id: '{channel_id}'"
                )
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.message(F.text.startswith("/sql_req "))
async def request_complete(message: Message):
    try:
        result = sql_request(message.text.lstrip("/sql_req "))
        await message.answer(text=str(result))
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.message(F.text.startswith("/sql_che "))
async def change_complete(message: Message):
    try:
        sql_changes(message.text.lstrip("/sql_che "))
        await message.answer(text="Ok")
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.message(F.text.startswith("/help"))
async def change_complete(message: Message):
    try:
        await message.answer(
            text="/code ''\n/add 'group_id' 'channel_id'\n/sql_req ''\n/sql_che ''"
        )
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))
