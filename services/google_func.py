import asyncio
import datetime

import gspread
import gspread_asyncio
from gspread.utils import rowcol_to_a1

from config_data.config import BASE_DIR, config
from database.db import User, History


from config_data.config import LOGGING_CONFIG
import logging.config

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('bot_logger')
err_log = logging.getLogger('errors_logger')


def read_user_from_table():
    json_file = BASE_DIR / 'credentials.json'
    gc = gspread.service_account(filename=json_file)
    url = config.tg_bot.USER_TABLE_URL
    sheet = gc.open_by_url(url)
    table = sheet.get_worksheet(0)
    values = table.get_values('A:T')[2:]
    # logger.debug(f'values: {values}')
    users = {}

    for row in values:
        try:
            # logger.debug(f'row: {row}')
            rieltor_code = row[0]
            phone = row[1] or '-'
            fio = row[2] or '-'
            date1 = row[4] or '1999-01-01'
            date2 = row[7] or '1999-01-01'
            date3 = row[10] or '1999-01-01'
            date4 = row[13] or '1999-01-01'
            date5 = row[16] or '1999-01-01'
            date6 = row[19] or '1999-01-01'
            # logger.debug(f'{rieltor_code, phone, fio, date1, date2, date3, date4, date5, date6}')
            users[rieltor_code] = {
                'phone': phone,
                'fio': fio,
                'date1': datetime.date.fromisoformat(date1),
                'date2': datetime.date.fromisoformat(date2),
                'date3': datetime.date.fromisoformat(date3),
                'date4': datetime.date.fromisoformat(date4),
                'date5': datetime.date.fromisoformat(date5),
                'date6': datetime.date.fromisoformat(date6),
            }
        except Exception as err:
            err_log.error(f'Ошибка при чтении строки {row}')
    return users

from google.oauth2.service_account import Credentials


def get_creds():
    # To obtain a service account JSON file, follow these steps:
    # https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account
    json_file = BASE_DIR / 'credentials.json'
    creds = Credentials.from_service_account_file(json_file)
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


async def read_stats_from_table():
    """
    Читает таблицу статистики пользователей.
    :return: Словарь со статистикой с ключом rieltor_code
    {'date': '11.09.2023',
     '133845': {'ФИО сотрудника': 'Альмаганбетов Алибек Дюсенбаевич', 'Категория': '0-3', 'Рейтинг': '15', 'Интегральный показатель': '81%', 'Заявки на покупку, план': '15', 'Заявки на покупку, факт': '30', 'Объекты в базе (активные), план': '30', 'Объекты в базе (активные), факт': '23', 'Консультации по ипотеке, план': '5', 'Консультации по ипотеке, факт': '4', 'Заявки в банк по ипотеке, план': '3', 'Заявки в банк, факт': '3', 'Подборки, план': '14', 'Подборки, факт': '42', 'Показы (покупатель), план': '9', 'Показы (покупатель), факт': '0'}, '1245788276': {'ФИО сотрудника': 'Алмазова Анна Дмитриевна', 'Категория': '4+', 'Рейтинг': '', 'Интегральный показатель': '', 'Заявки на покупку, план': '', 'Заявки на покупку, факт': '', 'Объекты в базе (активные), план': '', 'Объекты в базе (активные), факт': '', 'Консультации по ипотеке, план': '', 'Консультации по ипотеке, факт': '', 'Заявки в банк по ипотеке, план': '', 'Заявки в банк, факт': '', 'Подборки, план': '', 'Подборки, факт': '', 'Показы (покупатель), план': '', 'Показы (покупатель), факт': ''},
     '1233': {'ФИО сотрудника': 'Москвитин Антон Валерьевич', 'Категория': 'Первая неделя', 'Рейтинг': '', 'Интегральный показатель': '', 'Заявки на покупку, план': '', 'Заявки на покупку, факт': '', 'Объекты в базе (активные), план': '', 'Объекты в базе (активные), факт': '', 'Консультации по ипотеке, план': '', 'Консультации по ипотеке, факт': '', 'Заявки в банк по ипотеке, план': '', 'Заявки в банк, факт': '', 'Подборки, план': '', 'Подборки, факт': '', 'Показы (покупатель), план': '', 'Показы (покупатель), факт': '', 'Затраты на рекламу, план': '', 'Затраты на рекламу, факт': '', 'Город': 'Тюмень'}
    """
    agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
    agc = await agcm.authorize()
    url = config.tg_bot.USER_STAT_URL
    sheet = await agc.open_by_url(url)
    table = await sheet.get_worksheet(0)
    values = await table.get_values('A:U')
    columns_name = values[0]
    stat_dict = {}
    date = columns_name[0]
    stat_dict['date'] = date
    for row in values[1:]:
        user_dict = {}
        user_rieltor_code = row[1]
        for col_index, value in enumerate(row[2:], 2):
            key = columns_name[col_index]
            user_dict[key] = value
        stat_dict[user_rieltor_code] = user_dict
    return stat_dict



async def write_stats_from_table(rows):
    """
    Экспортирует данные пользователей User в таблицу сбор CSI
    :param rows:
    :return:
    """
    logger.debug(f'Добавляем {rows}')
    agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
    agc = await agcm.authorize()
    url = config.tg_bot.USER_TABLE_URL
    sheet = await agc.open_by_url(url)
    table = await sheet.get_worksheet(1)
    # await table.append_rows(rows)
    num_rows = len(rows)
    num_col = len(rows[0])
    logger.debug(f'{rowcol_to_a1(2 , 1)}:{rowcol_to_a1(1 + num_rows, num_col)}')
    await table.batch_update([{
        'range': f'{rowcol_to_a1(2 , 1)}:{rowcol_to_a1(1 + num_rows, num_col)}',
        'values': rows,
    }])


async def add_log_to_gtable(user: User, text: str):
    """
    Сохраняет движения пользователя в таблицу Логи
    :param user:
    :param text:
    :return:
    """
    try:
        logger.debug(f'Добавляем history в таблицу{text}')
        agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
        agc = await agcm.authorize()
        url = config.tg_bot.USER_TABLE_URL
        sheet = await agc.open_by_url(url)
        table = await sheet.get_worksheet(2)
        await table.append_row([
            datetime.datetime.now().isoformat(sep=' ')[:-7],
            user.username,
            text])
    except Exception as err:
        logger.debug(err)


async def read_msg_from_table() -> tuple[list, str]:
    """
    Читает таблицу "Рассылка сообщений"
    :return: список для рассылки и текст сообщения
    """
    agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
    agc = await agcm.authorize()
    url = config.tg_bot.USER_TABLE_URL
    sheet = await agc.open_by_url(url)
    table = await sheet.get_worksheet(3)
    text_cell = await table.cell(2, 3)
    text = text_cell.value
    senders = await table.get_values('A:A')
    return senders, text


if __name__ == '__main__':
    pass

    x = asyncio.run(read_stats_from_table())
    print(x.keys())

    # y = read_user_from_table()
    # print()
    # for u in y.items():
    #     print(u)
    #     break
    # print(y)
    # asyncio.run(write_stats_from_table())




