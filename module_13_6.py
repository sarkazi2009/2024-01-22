
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
api = '7531257871:AAGLFy_Y2D2_ji3KZNEJCr3tK01DCg0_v4c'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = InlineKeyboardMarkup()
kb1 = ReplyKeyboardMarkup()
button = InlineKeyboardButton(text='Расчитать норму калорий', callback_data='calories')
button1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formula')
kb.add(button)
kb.add(button1)
button2 = KeyboardButton(text='Расчитать')
button3 = KeyboardButton(text='Информация')
kb1.add(button2)
kb1.add(button3)
kb.resize_keyboard = True

@dp.message_handler(text=['/start'])
async def start(message):
    await message.answer("Привет", reply_markup=kb1)


@dp.message_handler(text=['Расчитать'])
async def start(message):
    await message.answer("Выбирите опцию", reply_markup=kb)


# @dp.callback_query_handler(text=['calories'])
# async def main_menu(message):
#     await message.answer('Введите свой возраст')

@dp.callback_query_handler(text=['formula'])
async def info(call):
    await call.message.answer('Формулы расчёта нормы калорий:\n'
                          '10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(г) + 5 - 161')
    await call.answer()

@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer('Бот расчитывает норму количество калорий для человека')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text=['calories'])
async def main_menu(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(
        f'Ваша норма калорий: {10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5}')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
