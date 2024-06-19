from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import *
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
    if callback.data == "start":
        await callback.message.edit_text(text="Привет, этот бот выдаст тебе ссылку на календарь твоей группы",
                                         reply_markup=keyboards.start())

    elif callback.data == "course_select":
        await callback.message.edit_text(text="Выбери курс",
                                         reply_markup=keyboards.courses())

    elif callback.data == "course_select_new":
        await callback.message.answer(text="Выбери курс",
                                      reply_markup=keyboards.courses(False))
        await callback.answer()

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
            if group.get('name') == name and len(group.get('subgroups')) == 0:
                await callback.message.edit_text(text=f"[Ссылка на календарь]({group.get('links')[0]})",
                                                 reply_markup=keyboards.finish(name),
                                                 parse_mode="MarkdownV2",
                                                 disable_web_page_preview=True
                                                 )

            elif group.get('name') == name:
                await callback.message.edit_text(text="Ссылки на календарь:\n" +
                                                      f"[Подгруппа {group.get('subgroups')[0]}]({group.get('links')[0]})\n" +
                                                      f"[Подгруппа {group.get('subgroups')[1]}]({group.get('links')[1]})",
                                                 reply_markup=keyboards.finish(name),
                                                 parse_mode="MarkdownV2",
                                                 disable_web_page_preview=True)

    elif callback.data == "eng_select":
        await callback.message.edit_text(text="Выбери свой курс по английскому",
                                         reply_markup=keyboards.eng_levels())

    elif callback.data == "eng_select_new":
        await callback.message.answer(text="Выбери свой курс по английскому",
                                      reply_markup=keyboards.eng_levels(False))
        await callback.answer()

    elif callback.data.startswith("level:"):
        name = callback.data.replace("level:", "")
        await callback.message.edit_text(text="Выбери группу",
                                         reply_markup=keyboards.eng_groups(name))

    elif callback.data.startswith("eng:"):
        name = callback.data.replace("eng:", "")
        await callback.message.edit_text(text=f"[Ссылка на календарь]({eng_groups[name]['link']})",
                                         reply_markup=keyboards.eng_finish(name),
                                         parse_mode="MarkdownV2",
                                         disable_web_page_preview=True
                                         )


async def main():
    await dp.start_polling(bot)


while True:
    try:
        run(main())
    except Exception as e:
        logging.error(e)
        sleep(30)
