from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import groups, API_TOKEN
import logging
from asyncio import run
from time import sleep
from bot.bot_modules import keyboards

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

logging.basicConfig(filename="logs/bot_logs.log", level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    encoding="utf8")
logging.info("START")


@dp.message(Command('start'))
async def start(message: types.message):
    await message.answer(text="Привет, этот бот выдаст тебе ссылку на календарь твоей группы",
                         reply_markup=keyboards.start())


@dp.callback_query()
async def callback_worker(callback: types.CallbackQuery):
    print(callback.data)
    if callback.data == "course_select":
        await callback.message.edit_text(text="Выбери курс",
                                         reply_markup=keyboards.courses())

    elif callback.data == "course_select_new":
        await callback.message.answer(text="Выбери курс",
                                      reply_markup=keyboards.courses())

    elif callback.data == "WIP":
        await callback.answer("В разработке")

    elif callback.data.startswith("course:"):

        await callback.message.edit_text(text="Выбери направление",
                                         reply_markup=keyboards.tracks(callback.data))

    elif callback.data.startswith("track:"):
        await callback.message.edit_text(text="Выберите группу",
                                         reply_markup=keyboards.groups(callback.data))

    elif callback.data.startswith("group:"):
        name = callback.data.replace("group:", "")
        for group in groups:
            if group.get('name') == name and len(group.get('subgroups')) == 1:
                await callback.message.edit_text(text=f"[Ваша ссылка]({group.get('links')[0]})",
                                                 reply_markup=keyboards.finish(name),
                                                 arse_mode="MarkdownV2",
                                                 disable_web_page_preview=True
                                                 )

            elif group.get('name') == name:
                await callback.message.edit_text(text="Ссылки на календарь:\n" +
                                                      f"[Подгруппа {group.get('subgroups')[0]}]({group.get('links')[0]})\n" +
                                                      f"[Подгруппа {group.get('subgroups')[1]}]({group.get('links')[1]})",
                                                 reply_markup=keyboards.finish(name),
                                                 parse_mode="MarkdownV2",
                                                 disable_web_page_preview=True)


async def main():
    await dp.start_polling(bot)


while True:
    try:
        run(main())
    except Exception as e:
        logging.error(e)
        sleep(30)
