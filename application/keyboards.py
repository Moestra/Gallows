from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Игры")],
                                     [KeyboardButton(text="Профиль")],
                                     [KeyboardButton(text="Настройки")]], 
                           resize_keyboard=True,
                           input_field_placeholder="Выбирите пункт меню...")

#games = InlineKeyboardMarkup(inline_keyboard=[
#  [InlineKeyboardButton(text="Игра Виселица", callback_data="game_gallows" )],
#    [InlineKeyboardButton(text="Игра в Города", callback_data="gane_cities")]],)

games = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Игра Виселица")],
                                      [KeyboardButton(text="Игра в Города")],
                                      [KeyboardButton(text="Назад")]],
                            resize_keyboard=True,
                            input_field_placeholder="Выбирите игру.....")


start_game = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Начать")]],
                                 resize_keyboard=True)