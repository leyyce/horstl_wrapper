from models.course import Course


class Day:

    date = "No information available"
    courses = []

    def __init__(self, dow: str, date: str):
        self.dow = dow
        self.date = date
        self.courses = []

    def add_course(self, course: Course):
        self.courses.append(course)

    def set_date(self, date: str):
        self.date = date
    
    def __str__(self, separator_length: int = 65):
        day_str = f"{self.dow.capitalize()} - {self.date}:\n"
        day_str += "-" * separator_length + "\n\n"
        if len(self.courses) > 0:
            for course in self.courses:
                day_str += "~" * separator_length + "\n"
                day_str += str(course) + "\n"
                day_str += "~" * separator_length + "\n" * 2
        else:
            day_str += "\tNothing to show here. Looks like a free day :)\n\n"
        day_str += "-" * separator_length
        return day_str
