from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from handlers.admin import on_startup

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)