import os

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re


BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=f'{BOT_TOKEN}')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserRegistration(StatesGroup):
    waiting_for_login = State()
    waiting_for_email = State()
    waiting_for_password = State()


@dp.message_handler(commands=['start'])
async def register_user(message: types.Message):
    await message.answer("Ласкаво просимо! Для реєстрації введіть свій логін")
    await UserRegistration.waiting_for_login.set()


@dp.message_handler(state=UserRegistration.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext):
    response = requests.get('http://web:8000/api/check-login/', params={'login': message.text})
    if response.status_code == 200:
        data = response.json()
        if data['is_unique']:
            await state.update_data(login=message.text)
            await message.answer("Введіть свою електронну пошту")
            await UserRegistration.waiting_for_email.set()
        else:
            await message.answer("Такий логін вже зайнятий, спробуйте інший")
    else:
        await message.answer("Помилка під час перевірки логіну")


email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@dp.message_handler(state=UserRegistration.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    if re.match(email_regex, message.text):
        response = requests.get('http://web:8000/api/check-email/', params={'email': message.text})
        if response.status_code == 200:
            data = response.json()
            if data['is_unique']:
                await state.update_data(email=message.text)
                await message.answer("Введіть пароль. ")
                await UserRegistration.waiting_for_password.set()
            else:
                await message.answer("Така пошта вже зайнята, спробуйте іншу")
        else:
            await message.answer("Помилка під час перевірки пошти")
    else:
        await message.answer("Неправильний формат пошти, введіть ще раз")


@dp.message_handler(state=UserRegistration.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        login = data['login']
        email = data['email']
        password = message.text

        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            await message.answer("Пароль повинен містити щонайменше одну цифру та одну літеру.")
            return

        if len(password) < 8:
            await message.answer("Пароль повинен містити щонайменше 8 символів.")
            return

        telegram_username = message.from_user.first_name
        telegram_id = message.from_user.username
        print(telegram_username, telegram_id)

        user_profile_photo = await bot.get_user_profile_photos(message.from_user.id)
        if len(user_profile_photo.photos[0]) > 0:
            file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
            avatar_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}'
            print(avatar_url)
        else:
            avatar_url = None
        print(avatar_url)

        session = requests.Session()
        response = session.get('http://web:8000/api/register-user/')
        csrf_token = response.cookies.get('csrftoken')

        response = session.post('http://web:8000/api/register-user/',
                                json={'login': login, 'email': email, 'password': password,
                                      'name': telegram_username, 'avatar_url': avatar_url,
                                      'tg_id': telegram_id},
                                headers={'X-CSRFToken': csrf_token})

        if response.status_code == 200:
            await message.answer("Реєстрацію завершено. Перейдіть на 46.175.149.43:4444 для авторизації Натисніть /start, щоб пройти реєстрацію знову.")
            await state.finish()
        else:
            await message.answer("Помилка під час реєстрації користувача. Натисніть /start, щоб розпочати заново.")
            await state.finish()


@dp.message_handler()
async def unknown_message(message: types.Message):
    await message.answer("Неправильна команда. Натисніть /start, щоб розпочати реєстрацію")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
