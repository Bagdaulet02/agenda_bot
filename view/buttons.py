from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mainMenu = InlineKeyboardMarkup(row_width=1)

inline_add_btn = InlineKeyboardButton('Добавить новую задачу', callback_data='add')
inline_done_btn = InlineKeyboardButton('Отметит задачу как выполненное', callback_data='done')
inline_list_btn = InlineKeyboardButton('Вывести список задач', callback_data='list')
inline_delete_btn = InlineKeyboardButton('Удалить задачу', callback_data='delete')

buttons = [inline_add_btn, inline_done_btn, inline_list_btn, inline_delete_btn]

mainMenu.add(*buttons)


tasksMenu = InlineKeyboardMarkup(row_width=2)

to_main_menu = InlineKeyboardButton('Вернутся в начальное меню', callback_data='mainMenu')

buttons = [inline_done_btn, inline_delete_btn, to_main_menu]

tasksMenu.add(*buttons)


