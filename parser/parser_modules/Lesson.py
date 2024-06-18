class Lesson(object):
    def __init__(self, name='', teacher_name='', location='', group='', start="01-01-1970T00:00+05:00",
                 end="01-01-1970T00:00+05:00"):
        self.name = name
        self.teacher_name = teacher_name
        self.location = location
        self.group = group
        self.start = {
            'dateTime': start,
            'timeZone': 'Asia/Yekaterinburg',
        }
        self.end = {
            'dateTime': end,
            'timeZone': 'Asia/Yekaterinburg',
        }

    def add_date(self, start, end):
        self.start = {
            'dateTime': start,
            'timeZone': 'Asia/Yekaterinburg',
        }
        self.end = {
            'dateTime': end,
            'timeZone': 'Asia/Yekaterinburg',
        }

    def get_dict(self):
        return {
            'summary': self.name,
            'description': self.teacher_name,
            'location': self.location,
            'start': self.start,
            'end': self.end,
            'group': self.group
        }
