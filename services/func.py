import asyncio
import datetime

from aiogram import Bot

from database.db import Session, User, Menu, History
from config_data.config import LOGGING_CONFIG, config

import logging.config

from services.google_func import read_stats_from_table

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('bot_logger')
err_log = logging.getLogger('errors_logger')


def check_user(id):
    """Возвращает найденных пользователей по tg_id"""
    logger.debug(f'Ищем юзера {id}')
    with Session() as session:
        user: User = session.query(User).filter(User.tg_id == str(id)).first()
        logger.debug(f'Результат: {user}')
        return user


def get_or_create_user(user) -> User:
    """Из юзера ТГ возвращает сущестующего User ли создает его"""
    try:
        tg_id = user.id
        username = user.username
        logger.debug(f'username {username}')
        old_user = check_user(tg_id)
        if old_user:
            logger.debug('Пользователь есть в базе')
            return old_user
        logger.debug('Добавляем пользователя')
        with Session() as session:
            new_user = User(tg_id=tg_id,
                            username=username,
                            register_date=datetime.datetime.now()
                            )
            session.add(new_user)
            session.commit()
            logger.debug(f'Пользователь создан: {new_user}')
        return new_user
    except Exception as err:
        err_log.error('Пользователь не создан', exc_info=True)


def update_user(tg_id, rieltor_code, g_user):
    logger.debug(f'Добавляем {(tg_id, rieltor_code, g_user)}')
    session = Session()
    with session:
        user: User = session.query(User).filter(User.tg_id == str(tg_id)).first()
        user.rieltor_code = rieltor_code
        for key, val in g_user.items():
            setattr(user, key, val)
        logger.debug(f'Юзер обновлен {user}')
        session.commit()


def get_menu_from_index(index) -> Menu:
    session = Session()
    with session:
        menu: Menu = session.query(Menu).filter(Menu.index == index).first()
        return menu


def write_log(user_id, text):
    session = Session()
    with session:
        history: History = History(user_id=user_id, text=text, time=datetime.datetime.now())
        session.add(history)
        session.commit()


def get_history(limit):
    session = Session()
    with session:
        historys = session.query(History).order_by(History.id.desc()).limit(limit).all()
        logger.debug(historys)
        return historys


def format_user_sats(user_dict, date: str):
    """{'ФИО сотрудника': 'Татьяна Кубышко Юрьевна',
     'Интегральный показатель': '76%', 'Заявки на покупку, план': '1',
     'Заявки на покупку, факт': '8', 'Объекты в базе (активные), план': '0',
     'Объекты в базе (активные), факт': '1',
     'Консультации по ипотеке, план': '0',
     'Консультации по ипотеке, факт': '0',
     'Заявки в банк по ипотеке, план': '0', 'Заявки в банк, факт': '0',
     'Подборки, план': '0', 'Подборки, факт': '7',
     'Показы (покупатель), план': '0', 'Показы (покупатель), факт': '0'}"""
    """
    - Заявки на покупку - 5 / 7
    - Объекты в базе (активные) - 2 / 54
    - Консультации по ипотеке - 3 / 8
    - Заявки в банк по ипотеке - 7 / 8
    - Подборки - 1 / 9
    - Показы (покупатель) - 5 / 5
    """
    logger.debug(user_dict)
    logger.debug(f'Форматируем статистику: {user_dict}')
    msg = (f'Ваши показатели на {date}*\n\n'
           f'<b>Показатель план / факт</b>\n'
           f"- Заявки на покупку - {user_dict['Заявки на покупку, план']} / {user_dict['Заявки на покупку, факт']}\n"
           f"- Объекты в базе (активные) - {user_dict['Объекты в базе (активные), план']} / {user_dict['Объекты в базе (активные), факт']}\n"
           f"- Консультации по ипотеке - {user_dict['Консультации по ипотеке, план']} / {user_dict['Консультации по ипотеке, факт']}\n"
           f"- Заявки в банк по ипотеке - {user_dict['Заявки в банк по ипотеке, план']} / {user_dict['Заявки в банк, факт']}\n"
           f"- Подборки - {user_dict['Подборки, план']} / {user_dict['Подборки, факт']}\n"
           f"- Показы (покупатель) - {user_dict['Показы (покупатель), план']} / {user_dict['Показы (покупатель), факт']}\n\n"
           f"<b>Интегральный показатель: {user_dict['Интегральный показатель']}</b>\n\n"
           )
    # msg = (
    #     f'Ваши показатели:\n'
    #     f'Дата*: {date}\n'
    # )
    # for key, val in user_dict.items():
    #     print(key)
    #     if key != 'ФИО сотрудника':
    #         msg += f'{key:32} {val}\n'
    msg += '*показатели обновляются раз в неделю по понедельникам'
    return msg


async def send_message_to_manager(bot, user, text_msg):
    await bot.send_message(
        chat_id=config.tg_bot.GROUP_ID,
        # chat_id='EtagiManagers',
        text=(
            f'{text_msg}\n\n'
            f'#id{user.tg_id}\n'
            f'{user.fio}'
        ),
        parse_mode='HTML'
    )


async def send_report_to_users(users_to_send: list[User], bot: Bot):
    user_stats = await read_stats_from_table()
    for user in users_to_send:
        try:
            if user.rieltor_code in user_stats:
                logger.debug(f'Стата пользователя {user} найдена')
                text = format_user_sats(user_stats[user.rieltor_code],
                                        user_stats['date'])
                await bot.send_message(user.tg_id, text)
                await asyncio.sleep(0.2)
                logger.info(f'Сообщение пользователю {user.fio or user.tg_id} отправлено')
        except Exception:
            await bot.send_message(config.tg_bot.admin_ids[0], 'Сообщение пользователю {user.fio or user.tg_id} НЕ отправлено')
            err_log.error(f'ошибка отправки сообщения пользователю {user.tg_id}', exc_info=False)