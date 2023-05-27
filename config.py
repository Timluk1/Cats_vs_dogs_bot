from client import Client
from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
client = Client(os.getenv("TOKEN"))
client.register_admin_handlers(client.dp)
executor.start_polling(client.dp, skip_updates=True)
