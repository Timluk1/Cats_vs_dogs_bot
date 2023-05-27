from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher.filters.state import Dispatcher
from cats_vs_dogs_model import prediction_model
from aiogram import types
import cv2
import numpy as np



class Client:
    def __init__(self, token):
        self.storage = MemoryStorage()

        self.bot = Bot(token=token)
        self.dp = Dispatcher(self.bot, storage=self.storage)


    async def start(self, message: types.Message):
        '''Стартовый вывод'''
        await self.bot.send_message(message.from_user.id,
                                    "Добро пожаловать в бота для распознования домашнего животного на фото!\nОтправьте фотографию, где изображена собака или кот, и бот даст вам ответ, кто изображен на фото.")
    async def get_image(self, message: types.Message):
        photo = message.photo[-1]  # Берем самую последнюю фотографию из списка
        photo_id = photo.file_id

        # Получаем содержимое файла в виде bytes
        file = await self.bot.get_file(photo_id)
        photo_bytes = await self.bot.download_file(file.file_path)

        # Создаем объект изображения в OpenCV
        nparr = np.frombuffer(photo_bytes.getbuffer(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        ans = prediction_model(image)
        if ans[0] == "Cat":
            await self.bot.send_message(message.from_user.id, f"На фотографии изображен кот")
        else:
            await self.bot.send_message(message.from_user.id, f"На фотографии изображена собака")

    def register_admin_handlers(self, dp: Dispatcher):
        '''Регестрируем все хэндлеры'''
        dp.register_message_handler(self.start, commands=["start"])
        dp.register_message_handler(self.get_image, content_types=types.ContentType.PHOTO)

