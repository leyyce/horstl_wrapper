from models.day import Day
from helpers.base.object_dict import ObjDict


class TimeTable:

    def __init__(self, student_name: str, cw: str):
        self.student_name = student_name
        self.cw = cw
        self.days = ObjDict({
            "monday": Day,
            "tuesday": Day,
            "wednesday": Day,
            "thursday": Day,
            "friday": Day,
            "saturday": Day,
        })

    def __str__(self):
        table_str = ""
        table_str += self.student_name + "\n" * 2
        table_str += self.cw + "\n" * 3
        for day in self.days.values():
            table_str += str(day) + "\n" * 3
        table_str = table_str[0:-3]
        return table_str
