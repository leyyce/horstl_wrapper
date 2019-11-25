from models.course import Course


class Day:

    date = None
    courses = None

    def __init__(self, dow: str, date: str):
        self.dow = dow
        self.date = date
        self.courses = []

    def add_course(self, course: Course):
        self.courses.append(course)

    def set_date(self, date: str):
        self.date = date
