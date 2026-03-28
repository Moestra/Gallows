from aiogram import  F , Router
from aiogram.types import Message , CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import application.keyboards as kb
import random

router = Router()

class Register(StatesGroup):
    name = State()
    age = State()
    

class Gallows(StatesGroup):
    playing = State()

with open("output_new.txt", "r", encoding="utf-8") as file:
    WORDS = [line.strip() for line in file]




@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Здесь со мной можно поиграть.Выбирай игру и погнали! \nСписок команд можно посмотреть /help", reply_markup=kb.main)
    
    
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("В боте есть следующие команды \n /stop --> завершение игры \n /help --> помощь \n /register --> добавить свой ник в бота")


@router.message(Command("register"))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("Введите ваше имя")


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer("Введите ваш возраст")


@router.message(Register.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer(f"Ваше имя: {data['name']}\nВаш возраст: {data['age']}")
    await state.clear()
    
    

    

@router.message(F.text == "Игры")
async def games(message: Message):
    await message.answer("Выберите игру", reply_markup=kb.games)


@router.message(F.text == "Назад")
async def home(message: Message):
    await message.answer("Вы вернулись в меню",reply_markup=kb.main)


    
@router.message(F.text == "Игра Виселица")
async def start_game(message: Message):
    await message.answer("Игра началась")
    await message.answer("ПРАВИЛА ИГРЫ: Суть игры отгадать слово. Кол-во черточек — это кол-во букв в слове. За каждую неправильную букву отнимается жизнь. Задача отгадать слово быстрее чем закончатся жизни.", reply_markup=kb.start_game)


    
@router.message(F.text == "Начать")
async def gallows_game(message: Message, state: FSMContext):
    word = random.choice(WORDS)
    so_cor = "_" * len(word)
    
    await state.update_data(
        word = word,
        max_attempts = 6,
        attempts = 0,
        used = [],
        so_cor = so_cor  
    )
        
    await message.answer("Добро пожаловать в Виселицу!")
    await message.answer(f"Слово на данный момент выглядит так: \n{' '.join(so_cor)}")
    await message.answer(f"Всего у вас 6 попыток")
    await message.answer("Введите свое предположение:")
    await state.set_state(Gallows.playing)



@router.message(Gallows.playing)
async def gallowa_gaming(message: Message, state: FSMContext):
    letter = message.text.strip().lower()
    data = await state.get_data()
    
    word = data['word']
    max_attempts = data['max_attempts']
    attempts = data['attempts']
    used = data['used']
    so_cor = data['so_cor']
    
    
    
    if attempts >= max_attempts:
        await message.answer(f"Игра уже завершена. Начните новую")
        await state.clear()
        return
      
    if len(letter) != 1:
        await message.answer("Извините, введите одну букву")
        await message.answer(f"Попыток осталось {max_attempts - attempts}")
        return
    
    if int(letter.isdigit()):
        await message.answer(f"Извините, {letter} это число. Введите букву")
        attempts +=1
        await message.answer(f"Попыток осталось {max_attempts - attempts}")
        if attempts >= max_attempts:
            await message.answer("Вы проиграли")
            await message.answer(f"Загаданное слово {word}")
            await state.clear()
        else:
            await state.update_data(attempts=attempts)
        return
    
    if letter in used:
        await message.answer(f"Вы уже вводили эту букву: '{letter.upper()}'")
        await message.answer(f"Попыток осталось {max_attempts - attempts}")
        return
    used.append(letter)
    
    if letter.lower() in word:
        new = ""
        for i in range(len(word)):
            if letter.lower() == word[i]:
                new += letter.lower()
            else:
                new += so_cor[i]
        so_cor = new
        await message.answer(f"Да, '{letter.upper()}' есть в слове")
        await message.answer(f"Слово выглядит так: {' '.join(so_cor)}")
        
        
        if so_cor == word:
            await message.answer("ПОБЕДА!!!")
            await message.answer(f"Загаданное слово: {word}")
            await state.clear()
            return
    
    
    else:
        await message.answer(f"Извините, '{letter.upper()}' этой буквы нет в слове")
        attempts +=1
        await message.answer(f"Попыток осталось {max_attempts - attempts}")

        if attempts >= max_attempts:
            await message.answer("Вы проиграли!")
            await message.answer(f"Загаданное слово: {word}")
            await state.clear()
            return
     
    await state.update_data(
        used = used,
        attempts=attempts,
        max_attempts = max_attempts,
        so_cor = so_cor
    )

@router.message(F.text == "Назад")
async def exit_menu(messenge: Message):
    await messenge.answer("Вы вернулись в меню", reply_markup=kb.games)


# @router.message(Command('stop'))
# async def cmd_stop(massege: Message, state: FSMContext):
#     stoping = await state.get_state()
#     if stoping is not None:
#         await state.clear()
#         await massege.answer("Вы завершили игру")
#         await massege.answer("Для того чтобы начать игру, нажмите кнопку Начать")
