from aiogram import F, Router, Bot
from aiogram.types import Message
from services.service import history_dict
from lexicon.lexicon import LEXICON
import logging

router: Router = Router()

logger = logging.getLogger(__name__)


@router.message(F.text.startswith("/send "))
async def send_answer(message: Message, bot: Bot):
    try:
        if message.chat.id in history_dict:
            channel_message = await bot.send_message(
                history_dict[message.chat.id].channel_id, message.text.lstrip("/send ")
            )
            history_dict[message.chat.id].add(
                message.message_id,
                channel_message.message_id,
            )
        else:
            if message.chat.type != "private":
                await message.answer(LEXICON["not_acctive_group"])
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.edited_message(F.text.startswith("/send "), F.chat.id.in_(history_dict))
async def edit_answer(message: Message, bot: Bot):
    try:
        if message.message_id in history_dict[message.chat.id]:
            result = history_dict[message.chat.id].search(message.message_id)
            await bot.edit_message_text(
                chat_id=history_dict[message.chat.id].channel_id,
                message_id=result[1],
                text=message.text.lstrip("/send "),
            )
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.message(
    F.text.startswith("/del"),
    F.chat.id.in_(history_dict),
)
async def del_message(message: Message, bot: Bot):
    try:
        if message.reply_to_message.message_id:
            if message.reply_to_message.from_user.id == message.from_user.id:
                if message.reply_to_message.text.startswith("/send "):
                    if (
                        message.reply_to_message.message_id
                        in history_dict[message.chat.id]
                    ):
                        result = history_dict[message.chat.id].search(
                            message.reply_to_message.message_id
                        )
                        await bot.delete_message(
                            message.chat.id, message.reply_to_message.message_id
                        )
                        await bot.delete_message(
                            history_dict[message.chat.id].channel_id, result[1]
                        )
                        history_dict[message.chat.id].delete(
                            message.reply_to_message.message_id
                        )
                    else:
                        await message.answer(LEXICON["del_old"])
                else:
                    await message.answer(LEXICON["del_not_mes"])
            else:
                await message.answer(LEXICON["del_not_his"])
        else:
            await message.answer(LEXICON["del_no_thread"])
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.message(
    F.text.startswith("/start"),
    F.chat.id.in_(history_dict),
)
async def start_client(message: Message):
    try:
        await message.answer(LEXICON["start_client"])
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.message(
    F.text.startswith("/help"),
    F.chat.id.in_(history_dict),
)
async def help_command(message: Message):
    try:
        await message.answer(LEXICON["help"])
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))


@router.message(F.text.startswith("/start"))
async def start_no_client(message: Message):
    try:
        await message.answer(LEXICON["start_no_client"])
        if message.chat.type != "private":
            await message.answer(f"Group id: {message.chat.id}")
    except Exception as err:
        logger.error(str(err))
        logger.error(message.model_dump_json(exclude_none=True))
