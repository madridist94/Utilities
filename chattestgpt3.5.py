import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json
import logging
from datetime import datetime

# Загрузка файла конфигурации с ключиками
file = open('config.json', 'r')
config = json.load(file)

# Установка ключа API и токена бота (которые в конфиге)
openai.api_key = config['openai']
bot = Bot(config['token'])

# Создание диспетчера
dp = Dispatcher(bot)

# Сбор и сохранение информации о пользователях, взаимодействующих с ботом
def load_users_data():
    try:
        with open('usergpt3-5.json', 'r', encoding='utf-8') as file:
            users_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users_data = {}
    return users_data



def save_users_data(users_data):
    with open('usergpt3-5.json', 'w', encoding='utf-8') as file:
        json.dump(users_data, file, indent=4, ensure_ascii=False)


users_data = load_users_data()


def update(user_id, message, role, content):
    user_id = str(user_id)  # Преобразование user_id в строку для совместимости с JSON
    if user_id not in users_data:
        users_data[user_id] = {
            "user_id": user_id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "last_interaction": datetime.now().isoformat(),
        }
        messages = [
            {"role": "system", "content": "Просто будь собой."},
            {"role": "user", "content": "Я клиент и задам тебе какой-нибудь вопрос по любой теме."},
            {"role": "assistant", "content": "Добро пожаловать в чат-бот!."},
        ]
    else:
        users_data[user_id]["last_interaction"] = datetime.now().isoformat()
        messages = users_data[user_id]["messages"] if "messages" in users_data[user_id] else []

    messages.append({"role": role, "content": content})

    save_users_data(users_data)
    return messages


@dp.message_handler()
async def send(message: types.Message):
    try:
        # Получение идентификатора пользователя
        user_id = message.from_user.id
        # Обновление сообщений пользователя
        messages = update(user_id, message, "user", message.text)

        # Добавление контекста для бота
        context_message = ""
        messages.append({"role": "user", "content": context_message})

        # Создание ответа с помощью GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Обновление истории сообщений для бота
        assistant_response = response['choices'][0]['message']['content']
        update(user_id, message, "assistant", assistant_response)

        # Отправка ответа пользователю
        await message.answer(assistant_response)

    except Exception as e:
        # Запись ошибки в журнал и отправка сообщения об ошибке пользователю
        logging.exception("Ошибка при обработке сообщения: %s", e)
        await message.answer("ОШИБКА: У ПЕНДОСОВ СНОВА ЧТО-ТО СЛОМАЛОСЬ :( . Попробуйте написать позже или попросить разработчика перезапустить бота.")

# Выведение информации о пользователях, взаимодействующих с ботом
def print_users_data():
    users_data = load_users_data()
    for user_id, user_data in users_data.items():
        print(f"User ID: {user_data['user_id']}\n"
              f"Username: {user_data['username']}\n"
              f"First name: {user_data['first_name']}\n"
              f"Last name: {user_data['last_name']}\n"
              f"Last interaction: {user_data['last_interaction']}\n\n")

# Запуск опроса ( данная строка кода запускает бесконечный цикл опроса, который прослушивает входящие
# сообщения и обрабатывает их с помощью указанных обработчиков.)
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)