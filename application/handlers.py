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


WORDS = ["огурец", "желтый", "автобус", "лето", "солнце", "мир"]




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

def display_world(word, guessed_word):
    display = ""
    for letter in word:
        if letter.lower() in guessed_word:
            display += letter.upper() 
        else:
            display = "_ " 
    return display.strip()

    
@router.message(F.text == "Начать")
async def gallows_game(message: Message, state: FSMContext):
    word = random.choice(WORDS)
    
    await state.update_data(
        word = word,
        attempts = 6,
        guessed_word = []    
    )
        
    await message.answer("Добро пожаловать в Виселицу!")
    await message.answer(f"Слово: {'_ ' *len(word)}")
    await message.answer(f"Оставшиеся попытки:6")
    await state.set_state(Gallows.playing)



@router.message(Gallows.playing)
async def gallowa_gaming(message: Message, state: FSMContext):
    letter = message.text.strip().lower()
    data = await state.get_data()
    
    word = data['word']
    attempts = data['attempts']
    guessed_word = data['guessed_word']
    
    if int(letter.isdigit()):
        await message.answer("Ошибка, введите букву")
        return 

    if len(letter) != 1:
        await message.answer("Введите одну букву")
        return 
    
    if letter in guessed_word:
        await message.answer("Вы уже вводили эту букву")
        return 
     
    guessed_word.append(letter)
    for i in guessed_word:
        await message.answer(f"Буква :{i}")
    
    if letter in word.lower():
        display = display_world(word, guessed_word)
        await message.answer("Эта буква есть в  слове")
        await message.answer(f"Слово:{display}")
        
        if '_' not in  display :
            await message.answer(f"Поздравляю!!!Вы отгадали слово: {word.upper()}")
            await state.clear()
            return
        
        elif letter not in word:
            attempts -= 1 
            await message.answer(f"Буквы {letter} нет в слове")
            await message.answer(f"Осталось попыток: {attempts}")
            display = display_world(word, guessed_word)
            await message.answer(f"Слово: {display}")
            
        if attempts <= 0:
            await message.answer(f"Вы проиграли, загаданное слово было:{word.upper()}") 
            await state.clear()
            return
        
     
        await state.update_data(
            guessed_word= guessed_word,
            attempts=attempts
        )

@router.message(Command('stop'))
async def cmd_stop(massege: Message, state: FSMContext):
    stoping = await state.get_state()
    if stoping is not None:
        await state.clear()
        await massege.answer("Вы завершили игру")
        await massege.answer("Для того чтобы начать игру, нажмите кнопку Начать")
