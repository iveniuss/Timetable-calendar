import datetime
from fnmatch import fnmatch
from parser.parser_modules.Lesson import Lesson
from config import mod_dates

TL_pat = '* ?.?. (*)'

WEEKDAYS = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")


def _format_date_time(start_time, end_time, date):
    if len(start_time) == 4:
        start_time = "0" + start_time
    if len(end_time) == 4:
        end_time = "0" + end_time
    start_time += ":00"
    end_time += ":00"
    day, month, year = date.split(".")
    date = f"{year}-{month}-{day}"
    return f'{date}T{start_time}+05:00', f'{date}T{end_time}+05:00'


def _compare_events(event1, event2):
    return all(event1[key] == event2[key] for key in event1 if key != 'id')


class Lessons(object):

    def __init__(self, group):
        self.lessons = []
        self.group_info = group

    def add_lessons_from_sheet(self, sheet):
        for row in range(4, sheet.max_row):
            lesson_cell = str(sheet.cell(row=row, column=self.group_info.get('column')).value)
            date_cell = str(sheet.cell(row=row, column=1).value)
            time_cell = str(sheet.cell(row=row, column=2).value)[3:]
            try:
                weekday, date = date_cell.split('\n')
                start_time, end_time = time_cell.split("-")
            except:
                continue

            for l in self._parse_lessons(lesson_cell):
                start, end = _format_date_time(start_time, end_time, date)
                l.add_date(start, end)
                self.lessons.append(l)

    def _split_groups(self, cell_value):
        cell_value = cell_value.replace('\n\n', '/double/')
        cell_value = cell_value.replace('\n', '/single/')
        subgroups = []

        if fnmatch(cell_value, '*/double/' + TL_pat + '/single/*/double/' + TL_pat):
            lessons = cell_value.split('/single/')
        elif fnmatch(cell_value, '*/double/' + TL_pat + '/single/' + TL_pat):
            subgroups = cell_value.split(';')
            subgroups[1] = subgroups[0][:subgroups[0].find('/double/')] + subgroups[1]
        elif fnmatch(cell_value, '*/single/' + TL_pat):
            cell_value = cell_value.replace('/single/', '/double/')
            subgroups = [cell_value]
        elif fnmatch(cell_value, '*/single/' + 'https://*'):
            cell_value = cell_value.replace('/single/', '/double/')
            subgroups = [cell_value]
        else:
            cell_value = cell_value.replace('/single/', ' ')
            subgroups = [cell_value]

        subgroup1 = self.group_info.get('subgroups')[0]
        subgroup2 = ''
        if len(self.group_info.get('subgroups')) == 2:
            subgroup2 = self.group_info.get('subgroups')[1]

        return subgroups, subgroup1, subgroup2

    def _parse_lessons(self, cell_value: str):

        subgroups, subgroup1, subgroup2 = self._split_groups(cell_value)

        for lesson_cell in subgroups:
            if lesson_cell[-2:] == f'{subgroup1})':
                subgroup = subgroup1
                lesson_cell = lesson_cell.replace(f', {subgroup1}', '')
            elif lesson_cell[-2:] == f'{subgroup2})':
                subgroup = subgroup2
                lesson_cell = lesson_cell.replace(f', {subgroup2}', '')
            else:
                subgroup = subgroup1 + subgroup2

            if lesson_cell.count('/double/') == 1:
                title, teacher_location = lesson_cell.split("/double/")
                if fnmatch(teacher_location, '(*)*(*)'):
                    close_scope = teacher_location.find(')')
                    teacher_location = teacher_location[close_scope + 1:]
                open_scope = teacher_location.find('(')
                close_scope = teacher_location.find(')')
                if open_scope != -1:
                    location = teacher_location[open_scope + 1:close_scope]
                    teacher = teacher_location[:open_scope - 1]
                else:
                    location = ''
                    teacher = teacher_location
            else:
                title = lesson_cell
                teacher = ''
                location = ''

            if "Английский язык" in title or title == "None":
                title = ''
            if "(ДОЦ)" in title:
                title = title.replace("(ДОЦ) ", "")

            if title != '':
                for g in subgroup:
                    yield Lesson(title, teacher, location, g)

    def get_lessons_dict(self, prev_timetable):
        actual_timetable = []
        for lesson in self.lessons:
            actual_timetable.append(lesson.get_dict())
        only_in_prev = [prev_event for prev_event in prev_timetable if
                        not any(_compare_events(prev_event, actual_event) for actual_event in actual_timetable)]

        only_in_actual = [actual_event for actual_event in actual_timetable if
                          not any(_compare_events(actual_event, prev_event) for prev_event in prev_timetable)]

        return {'to_add': only_in_actual,
                'to_del': only_in_prev}


class LessonsEng(object):

    def __init__(self):
        self.lessons = []

    def add_english_from_sheet(self, sheet):
        name = sheet.title
        first_day = None
        extra = ''
        if 'мод' in name and 'нед' in name:
            for module in mod_dates:
                if module in name:
                    first_day = mod_dates[module]
                    name = name.replace(module, '')
                    first_day = datetime.datetime(first_day['year'], first_day['month'], first_day['day'])
                    week_delta = datetime.timedelta(weeks=int(name[:name.find(' ')]) - 1)
                    break

        elif 'экзамен' in name.lower():
            extra = ' ЭКЗАМЕН'
            first_day = str(sheet.cell(row=2, column=4).value).strip()
            day, month, year = first_day.split('.')
            day = day[-2:]
            year = "20" + year[:-1]
            first_day = datetime.datetime(int(year), int(month), int(day))
            week_delta = datetime.timedelta(0)

        if first_day is None:
            return

        for row in range(4, sheet.max_row):
            lesson_cell = str(sheet.cell(row=row, column=3).value).strip()
            date_cell = str(sheet.cell(row=row, column=1).value).strip()
            time_cell = str(sheet.cell(row=row, column=2).value)
            time_cell = time_cell[time_cell.find('\n') + 1:].strip()
            if date_cell not in WEEKDAYS:
                continue
            time_delta = week_delta + datetime.timedelta(WEEKDAYS.index(date_cell))

            date = first_day + time_delta
            lessons = lesson_cell.split("\n")
            for lesson in lessons:
                if lesson.count('. ') < 2:
                    continue
                title, description = lesson.split(".", 1)
                description = description.replace('Ауд', 'ауд')
                description, location = description.split("ауд.")
                location = location.lower().replace(' ', '').replace(',к.', '[').strip() + "]"
                start_time, end_time = time_cell.split("-")
                date_str = date.date().strftime("%d.%m.%Y")
                start, end = _format_date_time(start_time, end_time, date_str)
                group = ''
                if "Деловой" in title:
                    group += 'Д'
                if "Базовый" in description:
                    group += 'БК-'
                elif "Основной" in description:
                    group += 'ОК-'
                elif "Продвинутый" in description:
                    group += 'ПК-'
                elif "начинающих" in title:
                    group += 'Н'
                if 'курс' in description:
                    index = description.find('курс')
                    course_num = description[index + 5:index + 6].strip()
                    group += course_num
                self.lessons.append(Lesson(title+extra, description.strip(), location, group, start, end))

    def get_lessons_dict(self, prev_timetable):
        actual_timetable = []
        for lesson in self.lessons:
            actual_timetable.append(lesson.get_dict())
        only_in_prev = [prev_event for prev_event in prev_timetable if
                        not any(_compare_events(prev_event, actual_event) for actual_event in actual_timetable)]

        only_in_actual = [actual_event for actual_event in actual_timetable if
                          not any(_compare_events(actual_event, prev_event) for prev_event in prev_timetable)]

        return {'to_add': only_in_actual,
                'to_del': only_in_prev}
