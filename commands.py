from bot_config import dp, bot
from aiogram import types
import random

totalNumberOfSweets = 150

new_game = False

# step1 = random.randint(0, 1) # 0 - первым ходит человек, 1 - первым ходит бот
step1 = 0




async def bot_turn(message):
    global totalNumberOfSweets
    if totalNumberOfSweets > 28:
        take = random.randint(1, 28)
    else:
        take = totalNumberOfSweets
    totalNumberOfSweets -= take
    if totalNumberOfSweets > 0:
        await bot.send_message(message.from_user.id, text=f'Бот взял {take} конфет, на столе осталось '
                                                      f'{totalNumberOfSweets} конфет')
    else:
        await bot.send_message(message.from_user.id, text=f'Бот взял {take} конфет, бот выиграл!')

async def player_turn(message):
    await bot.send_message(message.from_user.id,
                           text=f'{message.from_user.first_name}, теперь Ваш ход')


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name}, '
                                                      f'Вы написали мне "{message.text}". \n'
                                                      f'Для старта игры в "Конфеты" введите команду "/Начало".')

@dp.message_handler(commands=['Начало'])
async def start_bot(message: types.Message):
    global new_game
    new_game = True
    global step1
    if step1 == 0:
        await bot.send_message(message.from_user.id, text=f'Условия игры следующие. На столе лежит 150 конфет. '
                                                          f'Играют игрок против бота. Первый ход определяется '
                                                          f'жеребьёвкой. За один ход можно забрать не более 28 конфет. '
                                                          f'Все конфеты оппонента достаются сделавшему последний ход. \n \n'
                                                          f'По результатам жеребьёвки первым ходите Вы. \n \n'
                                                          f'Введите количество конфет, которое собираетесь взять '
                                                          f'(не более 28 штук)')
    else:
        await bot.send_message(message.from_user.id, text=f'По результат жеребьёвки первым ходит бот')


@dp.message_handler()
async def start_bot(message: types.Message):
    global totalNumberOfSweets
    global new_game
    if new_game == True:
        if totalNumberOfSweets > 0:
            name = message.from_user.first_name
            text = message.text
            if (message.text.isdigit()) and (int(message.text) in range(1, 29)):
                totalNumberOfSweets -= int(message.text)
                if totalNumberOfSweets > 0:
                    await bot.send_message(message.from_user.id,
                                            text=f'{name} взял {text} конфет, на столе осталось {totalNumberOfSweets} '
                                                f'конфет')
                else:
                    await bot.send_message(message.from_user.id,
                                           text=f'{name} взял {text} конфет, поздравляем, Вы выиграли!')
                if totalNumberOfSweets > 0:
                    await bot_turn(message)
                if totalNumberOfSweets > 0:
                    await player_turn(message)

            else:
                await bot.send_message(message.from_user.id, text=f'Напишите число конфет, которое хотите взять '
                                                                  f'(от 1 до 28 штук)')
