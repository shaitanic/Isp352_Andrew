import os
from pydub import AudioSegment
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Инициализируем бота и диспетчера
TOKEN = "token"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Обработчик команды /start
    await message.reply("Привет! Отправьте мне файл формата MP4, и я конвертирую его в MP3.")

@dp.message_handler(content_types=['document'])
async def convert_to_mp3(message: types.Message):
    # Обработчик отправленных файлов
    if message.document.mime_type == 'video/mp4':
        # Скачиваем и сохраняем файл
        await message.document.download('input.mp4')

        # Конвертация MP4 в MP3
        audio = AudioSegment.from_file("input.mp4", "mp4")
        audio.export("output.mp3", format="mp3")

        # Отправляем конвертированный файл
        with open("output.mp3", "rb") as audio_file:
            await message.reply_audio(audio_file)

        # Удаляем временные файлы
        os.remove("input.mp4")
        os.remove("output.mp3")
    else:
        await message.reply("Пожалуйста, отправьте файл формата MP4.")


if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)