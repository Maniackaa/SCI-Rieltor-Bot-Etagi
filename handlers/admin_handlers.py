import asyncio

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter, Text, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import CallbackQuery, Message
from config_data.config import config
from database.db import History
from keyboards.keyboards import yes_no_kb
from services.db_func import get_users_to_send_message, get_user_from_rieltor_code
from services.func import get_history


from config_data.config import LOGGING_CONFIG
import logging.config

from services.google_func import read_msg_from_table

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('bot_logger')
err_log = logging.getLogger('errors_logger')


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admins = config.tg_bot.admin_ids

    async def __call__(self, message: Message) -> bool:
        print(f'Проверка на админа\n'
              f'{message}\n'
              f'{message.from_user.id} in {self.admins}\n')
        return message.from_user.id in self.admins


router = Router()
router.message.filter(IsAdmin())


class FSMAdmin(StatesGroup):
    send_message = State()
    send_message_from_table = State()


@router.message(Command(commands=["history"]))
async def info(message: Message):
    history_list: list[History] = get_history(10)
    for hist in history_list:
        await message.answer(f'{hist.time}\n{hist.text}')


@router.message(Command(commands=["send_to_all"]))
async def command_send_to_all(message: Message,  state: FSMContext):
    await message.answer('Введите текст для рассылки всем пользователям:')
    await state.set_state(FSMAdmin.send_message)


# Обработка send_to_all
@router.message(StateFilter(FSMAdmin.send_message))
async def send_to_all(message: Message, state: FSMContext, bot: Bot):
    text = message.text
    users = get_users_to_send_message()
    for user in users:
        try:
            await bot.send_message(user.tg_id, text)
            await message.answer(F'Сообщение пользователю {user.fio or user.tg_id} отправлено')
            await asyncio.sleep(0.2)
            logger.info(f'Сообщение пользователю {user.fio or user.tg_id} отправлено')
        except Exception:
            await message.answer(f'Сообщение пользователю {user.fio or user.tg_id} НЕ отправлено')
            err_log.error(f'ошибка отправки сообщения пользователю {user.tg_id}', exc_info=False)
    await state.clear()


@router.message(Command(commands=["send"]))
async def command_send_to_all(message: Message,  state: FSMContext):
    senders, text = await read_msg_from_table()
    q_text = f'Список для отправки:\n'
    users = set()
    for sender in senders:
        user = get_user_from_rieltor_code(sender[0])
        if user:
            users.add(user)
            q_text += user.fio + '\n'
    await message.answer(q_text)
    await message.answer(f'Сообщение для отправки:\n\n {text}')
    await message.answer('Отправить сообщение?', reply_markup=yes_no_kb(2))
    await state.set_state(FSMAdmin.send_message_from_table)
    await state.update_data(users=users, text=text)


# Обработка send yes/no
@router.callback_query(StateFilter(FSMAdmin.send_message_from_table))
async def csi_answer(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if callback.data == 'yes':
        data = await state.get_data()
        users = data['users']
        text = data['text']
        print(users)
        for user in users:
            try:
                if user and user.tg_id:
                    await bot.send_message(user.tg_id, text=text)
                    logger.info(f'Сообщение для {user} отправлено')
                    await asyncio.sleep(0.2)
                else:
                    logger.warning(f'Не могу отправить сообщения для {user} - id не найден')
            except Exception:
                err_log.error(f'Сообщение для {user} НЕ отправлено', exc_info=False)
    await callback.message.delete()
    await state.clear()


