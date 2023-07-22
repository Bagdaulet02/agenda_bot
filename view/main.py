from sys import path
path.append('')
path.append('')

import config
import controller
import buttons
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


class TaskHandler(StatesGroup):
    title = State()
    description = State()

class IndexHandler(StatesGroup):
    task_index = State()


@dp.message_handler(commands=['start'])
async def start(message):
    text = "Добрый день!\nЧего желаете?"
    await bot.send_message(message.from_user.id, text, reply_markup=buttons.mainMenu)


@dp.callback_query_handler(text='add')
async def add(callback):
    title = ''
    descriiption = ''
    chat_id = callback.from_user.id
    await TaskHandler.title.set()
    await bot.send_message(chat_id, text='Введите название задачи:')


    @dp.message_handler(state=TaskHandler.title)
    async def title(message, state):
        await state.update_data(title=message.text)

        await TaskHandler.next()
        await bot.send_message(chat_id, text='Введите описание задачи:')

    @dp.message_handler(state=TaskHandler.description)
    async def description(message, state):
        await state.update_data(description=message.text)
        data = await state.get_data()
        task_index = controller.addTask(data['title'], data['description'])
        text = f"Индекс вашей задачи: {task_index}"
        await bot.send_message(chat_id, text, reply_markup=buttons.mainMenu)
        await state.finish()


@dp.callback_query_handler(text='done')
async def done(callback):
    task_index = 0
    task_status = ''
    text = ''
    chat_id = callback.from_user.id
    await bot.send_message(chat_id, text='Введите индекс задачи:')
    await IndexHandler.task_index.set()


    @dp.message_handler(state=IndexHandler.task_index)
    async def indexHandler(message, state):
        try:
            await state.update_data(task_index = int(message.text))
        except ValueError:
            text = "Неверный формат индекса!"
            await state.update_data(task_index = 0)
        tmp = await state.get_data();
        task_index = tmp['task_index']

        if task_index != 0:
            task = controller.setDone(task_index)
            if task == 0:
                text = "Неверный формат индекса"
            else:
                text = f"Статус задачи {task_index}: Выполнена"

        await bot.send_message(chat_id, text, reply_markup=buttons.mainMenu)
        await state.finish()


@dp.callback_query_handler(text='list')
async def tasksList(callback):
    text = ''
    tasks = controller.getAllTasks()
    if tasks == 0:
        text = "Задач нет"
    else:
        for task in tasks:
            text_tmp = f"Задача: {task.task_index}\n\n{task.task_title}\n\n{task.task_description}\n\nСтатус: {task.task_status}\n\n\n"
            text += text_tmp
    await bot.send_message(callback.from_user.id, text, reply_markup=buttons.tasksMenu)


@dp.callback_query_handler(text='delete')
async def delete(callback):
    task_index = 0
    text = ''
    chat_id = callback.from_user.id
    await bot.send_message(chat_id, text='Введите индекс задачи:')
    await IndexHandler.task_index.set()

    @dp.message_handler(state=IndexHandler.task_index)
    async def indexHandler(message, state):
        try:
            await state.update_data(task_index = int(message.text))
        except ValueError:
            text = "Неверный формат индекса!"
            task_index = 0
        task_index = await state.get_data()
        await state.finish()

        task = controller.find(task_index['task_index'])
        if task == None:
            await bot.send_message(chat_id, "По заданному индексу ничего не найдено", reply_markup=buttons.mainMenu)
        else:
            controller.delete(task)
            await bot.send_message(chat_id, f"Задача {task_index['task_index']} удалена", reply_markup=buttons.mainMenu)

@dp.callback_query_handler(text='mainMenu')
async def mainMenu(callback):
    await bot.send_message(callback.from_user.id, "Чего желаете?", reply_markup=buttons.mainMenu)


if __name__ == '__main__':
    executor.start_polling(dp)

