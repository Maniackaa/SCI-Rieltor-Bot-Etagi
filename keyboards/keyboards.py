from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,\
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db import Session, Menu


kb = [

    [KeyboardButton(text="Меню")],
    ]

start_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=kb,
                                                    resize_keyboard=True)


contact_kb_buttons = [
    [KeyboardButton(
        text="Отправить номер телефона",
        request_contact=True
    )],
    ]

contact_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=contact_kb_buttons,
    resize_keyboard=True)

def start_menu_kb(width: int, parent_id) -> InlineKeyboardMarkup:
    if parent_id == '0':
        parent_id = None
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = []
    session = Session()
    with session:
        start_menu_items: list[Menu] = session.query(Menu).filter(
            Menu.parent_id == parent_id).order_by(Menu.index).all()
    for num, menu_item in enumerate(start_menu_items, 1):
        callback_button = InlineKeyboardButton(
            text=(menu_item.text + ' ➥' if menu_item.is_with_children else menu_item.text),
            callback_data=f'startmenu:{menu_item.index}')
        buttons.append(callback_button)
    # back
    if parent_id:
        back_button = InlineKeyboardButton(
            text='⇤ Назад',
            callback_data=f'startmenu:0')
        buttons.append(back_button)
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()


# start_menu_kb(1, None)


def csi_kb(width: int, date_day) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = [
        '1 - ХУЖЕ НЕКУДА',
        '2 - ПЛОХО',
        '3 - НЕПЛОХО',
        '4 - ХОРОШО',
        '5 - ОТЛИЧНО'
    ]
    kb_buttons = []
    for num,  button_text in enumerate(buttons, 1):
        callback_button: InlineKeyboardButton = InlineKeyboardButton(
            text=button_text, callback_data=f'CSI_answer:{date_day}:{num}')
        kb_buttons.append(callback_button)
    kb_builder.row(*kb_buttons, width=width)
    return kb_builder.as_markup()


def yes_no_kb(width: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text='Да', callback_data='yes'),
        InlineKeyboardButton(text='Нет', callback_data='no'),
    ]
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()

# csi_kb(1, dat)