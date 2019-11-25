from models.course import Course
from models.day import Day


class TimeTable:

    def __init__(self, student_name: str, cw: str):
        self.student_name = student_name
        self.cw = cw
        self.days = {
            "monday": Day,
            "tuesday": Day,
            "wednesday": Day,
            "thursday": Day,
            "friday": Day,
            "saturday": Day,
        }

    def to_string(self):
        table_str = ""
        table_str += self.student_name + "\n" * 2
        table_str += self.cw + "\n" * 3
        for day_name, day in self.days.items():
            table_str += f"{day_name.capitalize()} - {day.date}:\n\n"
            if len(day.courses) > 0:
                for course in day.courses:
                    table_str += f"\tName: {course.name}\n\tTyp: {course.kind}\n\t" \
                                 f"Parralelgruppe: {course.group}\n\tZeit: {course.time}\n\t" \
                                 f"Frequenz: {course.frequency}\n\tZeitraum: {course.time_period}\n\t" \
                                 f"Rauminfo: {course.room_info}\n\tDozent/in: {course.docent}\n\t" \
                                 f"Status: {course.status}"
                    table_str += f"\n\tWarnung: {course.warning}\n\n" if course.warning is not "None" else "\n\n"
            else:
                table_str += "\tNothing to show here. Looks like a free day :)"
            table_str += "\n" * 2

        return table_str
