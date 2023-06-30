from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from tabulate import tabulate

import protocol
from cfg import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def help(message: types.Message):
    await bot.send_message(message.chat.id,
                            'Доступные команды:\n\n'
                            '👀 Для просмотря доступных команд: <u><b>/help</b></u>\n'
                            '✅ Для добавления спортсмена: <u><b>/add</b></u>\n'
                            '❌ Для удаления спортсмена: <u><b>/del</b></u>\n'
                            '✉ Для отправки текущего протокола на почту: <u><b>/send</b></u>\n'
                            '💣 Для ПОЛНОЙ очистки базы данных: <u><b>/del_all</b></u>',
                            parse_mode="HTML")

@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    await bot.send_message(message.chat.id, '💬 Введите данные в формате: Нагрудный номер, ФИО, пол, возраст, вид, результат')

@dp.message_handler(commands='del')
async def delite(message: types.Message):
    await message.answer(text = '💬 Введите номер спортсмена для удаления')

@dp.message_handler(commands='del_all')
async def delete_all(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb1 = KeyboardButton('Да')
    kb2 = KeyboardButton('Нет')
    kb.add(kb1, kb2)
    await message.answer(text = '❗❗❗ Дальнейшие действия приведут к полной и БЕЗВОЗВРАТНОЙ очистке базы данных!. Продолжить? ❗❗❗',
                         reply_markup=kb)

@dp.message_handler(commands='send')
async def send(message: types.Message):
    res = protocol.send()
        
    with open('tosend.txt', 'w+') as pr_file:
        headers = ['Номер', 'ФИО', 'Пол', 'Возраст', 'Вид', 'Результат']
        pr_file.write(tabulate(res, headers=headers, tablefmt='grid'))

    try:
        with open('tosend.txt', 'rb') as prtocol_file:    
            await message.answer_document(prtocol_file)
    except:
        await message.answer(text = 'Что-то пошло не так!')

@dp.message_handler()
async def tobd(message: types.Message):

    if message.text.__contains__(','):
        arr = message.text.split(',')
        if len(arr) != 6:
            await message.answer(text='🚫Что-то пошло не так. Проверьте данные!')
        else:
            reuslt_add = protocol.add_sport(arr)
            await message.answer(text=reuslt_add)

    elif message.text == 'Да':
        protocol.del_all()
        await message.answer(text = 'База данных очищена!', reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Нет':
        await message.answer(text = 'Действие отменено', reply_markup=ReplyKeyboardRemove())

    else:
        try:
            int(message.text)
            result_del = protocol.del_sport(message.text)
            await message.answer(text=result_del)
        except:
            await message.answer(text = '🚫Что-то пошло не так, проверьте даныные!')
    

async def on_startup(_):
    print('Работаем')

async def on_shutdown(_):
    print('НЕ работаем')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)

#ДОБАВИТЬ КНОПКИ СБОКУ ДЛЯ БЫСТРОГО НАБОРА