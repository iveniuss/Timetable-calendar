from config import *
from parser.parser_modules.GoogleCalendar import GoogleCalendar
from parser.parser_modules.Lessons import Lessons, LessonsEng
from parser.parser_modules.Timetable import Timetable
import datetime
import logging
from time import sleep

logging.basicConfig(filename="logs/calendar_logs.log", level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    encoding="utf8")

UPDATE_TIME = 7200

calendar = GoogleCalendar()
timetable = Timetable()

logging.info("--START--")
while True:
    try:

        start_time = datetime.datetime.now()

        timetable.update_timetable()

        for group in groups:
            start_time_gr = datetime.datetime.now()
            lessons = Lessons(group)
            for workbook in timetable.get_workbooks():
                worksheet = workbook[f"{group.get('course')} курс"]
                lessons.add_lessons_from_sheet(worksheet)

            prev_timetable = calendar.get_list_dict(group['ids'][0])
            if len(group['ids']) == 2:
                prev_timetable += calendar.get_list_dict(group['ids'][1])

            events = lessons.get_lessons_dict(prev_timetable)

            for event in events['to_add']:
                cal_id = group['ids'][group['subgroups'].find(event['group'])]
                calendar.create_event(event, cal_id)

            for event in events['to_del']:
                cal_id = group['ids'][group['subgroups'].find(event['group'])]
                calendar.delete_id(event['id'], cal_id)

            logging.info(f"{group['name']} calendar updated({datetime.datetime.now() - start_time_gr})")

        start_time_eng = datetime.datetime.now()

        lessons = LessonsEng()

        for workbook in timetable.get_workbooks_eng():
            worksheets = workbook.sheetnames
            if len(worksheets) >= 3:
                lessons.add_english_from_sheet(workbook[worksheets[-2]])
                lessons.add_english_from_sheet(workbook[worksheets[-1]])
            else:
                lessons.add_english_from_sheet(workbook[worksheets[-1]])

        prev_timetable = []
        for eng_group in eng_groups:
            prev_timetable += calendar.get_list_dict(eng_groups[eng_group]['id'])

        events = lessons.get_lessons_dict(prev_timetable)

        for event in events['to_add']:
            if event['group'] in eng_groups:
                cal_id = eng_groups[event['group']]['id']
                calendar.create_event(event, cal_id)

        for event in events['to_del']:
            if event['group'] in eng_groups:
                cal_id = eng_groups[event['group']]['id']
                calendar.delete_id(event['id'], cal_id)

        logging.info(f"English timetable updated ({datetime.datetime.now() - start_time_eng})")

        duration = datetime.datetime.now() - start_time
        sleep(UPDATE_TIME - duration.total_seconds())
    except Exception as ex:
        logging.error(ex)
        sleep(30)
