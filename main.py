import asyncio

import aioschedule
import schedule
from aiogram import Bot, Dispatcher

from config_data.config import LOGGING_CONFIG, config
from handlers import user_handlers, echo, csi_handlers, admin_handlers

import logging.config

from handlers.csi_handlers import send_csi_to_users
from services.CSI import find_users_to_send, find_users_to_send_report
from services.func import send_report_to_users

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('bot_logger')
err_log = logging.getLogger('errors_logger')


async def csi_job(bot):
    # Запрос анкетирования CSI
    users_to_send = find_users_to_send()
    logger.debug(f'Сегодня найдены пользовтаели для рассылки CSI:\n{users_to_send}')
    await send_csi_to_users(bot, users_to_send)


# async def csi_first_days(bot):
#     # Запрос анкетирования CSI
#     users_to_send = find_10days_users()
#     logger.debug(f'Сегодня найдены пользовтаели для рассылки новеньких CSI:\n{users_to_send}')
#     await send_csi_to_users(bot, users_to_send)


async def send_report(bot):
    # Рассылка статистики каждый вторник
    users_to_send_report = find_users_to_send_report()
    logger.debug(f'Сегодня найдены пользовтаели для рассылки CSI:\n{users_to_send_report}')
    await send_report_to_users(users_to_send_report, bot)


async def shedulers(bot):
    # aioschedule.every(5).minutes.do(job, bot)
    time_start = '9:00'
    aioschedule.every().day.at(time_start).do(csi_job, bot)
    aioschedule.every().tuesday.at('11:00').do(send_report, bot)
    # aioschedule.every().minute.do(send_report, bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    logger.info('Starting bot Etagi')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Регистриуем
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(csi_handlers.router)
    dp.include_router(echo.router)
    asyncio.create_task(shedulers(bot))
    # asyncio.create_task(job(bot))
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await bot.send_message(
            config.tg_bot.admin_ids[0], f'Бот Этажи запущен.')
    except:
        err_log.critical(f'Не могу отравить сообщение {config.tg_bot.admin_ids[0]}')
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped!')