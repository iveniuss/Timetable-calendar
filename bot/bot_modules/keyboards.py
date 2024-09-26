from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import groups as groups_info
from config import eng_groups as eng_groups_info

COURSES_SHIFT = 25


def _start():
    builder = InlineKeyboardBuilder()
    builder.button(text='Выбор курсов', callback_data='course_select')
    # builder.button(text='Выбор английского', callback_data='eng_select') Отложено до лучших времен
    builder.button(text='Помощь', url="https://iveniuss.notion.site/Google-590edc08e8a645128dd7ccd6a35df734?pvs=4")
    builder.adjust(1)
    return builder


def start():
    return _start().as_markup()


def courses(back_button=True):
    builder = InlineKeyboardBuilder()
    for i in range(1, 5):
        builder.button(text=str(i), callback_data="course:" + str(COURSES_SHIFT - i))
    if back_button:
        builder.button(text='< Назад  ', callback_data="start")
    builder.adjust(2)
    return builder.as_markup()


def tracks(course):
    course = course.replace('course:', '')
    tracks_list = ()
    builder = InlineKeyboardBuilder()

    if course == "23" or course == "22":
        tracks_list = ("РИС", "МБ", "И", "Ю", "ИЯ")
    # elif course == "21":
    #     tracks_list = ("ПИ", "БИ", "Э", "УБ", "И", "Ю", "ИЯ")
    # elif course == "20":
    #     tracks_list = ("И", "Ю")

    for track in tracks_list:
        builder.button(text=track, callback_data=f"track:{track}-{course}")

    builder.button(text='< Назад  ', callback_data='course_select')
    builder.adjust(2)
    return builder.as_markup()


def groups(track):
    track = track.replace('track:', '')
    builder = InlineKeyboardBuilder()
    count = 0

    for gr in groups_info:
        if gr['name'][:-2] == track:
            count += 1

    if count == 0:
        builder.button(text='потом тут будут группы', callback_data='WIP')

    for i in range(1, count + 1):
        builder.button(text=str(i), callback_data=f"group:{track}-{i}")

    builder.button(text='< Назад  ', callback_data=f'course:{track[-2:]}')
    builder.adjust(2)
    return builder.as_markup()


def eng_levels(back_button=True):
    builder = InlineKeyboardBuilder()
    builder.button(text="Базовый", callback_data="level:БК")
    builder.button(text="Основной", callback_data="level:ОК")
    builder.button(text="Продвинутый", callback_data="level:ПК")
    builder.button(text="Деловой Основной", callback_data="level:ДОК")
    builder.button(text="Деловой Продвинутый", callback_data="level:ДПК")
    builder.button(text='Для начинающих', callback_data="level:Н")
    if back_button:
        builder.button(text='< Назад  ', callback_data="start")
    builder.adjust(1)
    return builder.as_markup()


def eng_groups(name):
    builder = InlineKeyboardBuilder()
    groups_count = 0
    for gr in eng_groups_info:
        if gr.startswith(name):
            groups_count += 1
    if groups_count == 0:
        builder.button(text="тут будут группы", callback_data="WIP")

    for i in range(1, groups_count + 1):
        builder.button(text=str(i), callback_data=f"eng:{name}-{i}")

    builder.button(text='< Назад  ', callback_data=f'eng_select')
    builder.adjust(2)
    return builder.as_markup()


def finish(group):
    builder = _start()
    builder.button(text='< Назад  ', callback_data=f"track:{group[:-2]}")
    builder.adjust(1)
    return builder.as_markup()


def eng_finish(group):
    builder = _start()
    builder.button(text='< Назад  ', callback_data=f"level:{group[:group.rfind('-')]}")
    builder.adjust(1)
    return builder.as_markup()
