from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import groups as groups_info
from config import eng_groups as eng_groups_info

COURSES_SHIFT = 24


def start():
    builder = InlineKeyboardBuilder()
    builder.button(text='Выбор курсов', callback_data='course_select')
    builder.button(text='Выбор английского', callback_data='eng_select')
    builder.button(text='Помощь', url="https://hsecalendarhelp.tiwri.com/")
    builder.adjust(1)
    return builder.as_markup()


def courses():
    builder = InlineKeyboardBuilder()
    for i in range(1, 5):
        builder.button(text=str(i), callback_data="course:" + str(COURSES_SHIFT - i))
    builder.button(text='< Назад  ', callback_data="start")
    builder.adjust(2)
    return builder.as_markup()


def tracks(course):
    course = course.replace('course:', '')
    tracks_list = ()
    builder = InlineKeyboardBuilder()

    if course == "23" or course == "22":
        tracks_list = ("РИС", "МБ", "И", "Ю", "ИЯ")
    elif course == "21":
        tracks_list = ("ПИ", "БИ", "Э", "УБ", "И", "Ю", "ИЯ")
    elif course == "20":
        builder.button(text="тут будут направления", callback_data="WIP")

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


def eng_levels():
    builder = InlineKeyboardBuilder()
    builder.button(text="Базовый", callback_data="level:БК")
    builder.button(text="Основной", callback_data="level:ОК")
    builder.button(text="Продвинутый", callback_data="level:ПК")
    builder.button(text="Деловой Основной", callback_data="level:ДОК")
    builder.button(text="Деловой Продвинутый", callback_data="level:ДПК")
    builder.button(text='Для начинающих', callback_data="level:Н")
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
    builder = InlineKeyboardBuilder()
    builder.button(text='Выбрать группу', callback_data='course_select_new')
    builder.button(text='Выбрать английский', callback_data='eng_select_new')
    builder.button(text='Помощь', url="https://hsecalendarhelp.tiwri.com/")
    builder.button(text='< Назад  ', callback_data=f"track:{group[:-2]}")
    builder.adjust(2)
    return builder.as_markup()
