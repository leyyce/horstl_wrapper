from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup

from models.day import Day
from models.course import Course
from models.time_table import TimeTable


class Scrapper:

    @dataclass
    class PageIds:
        HOMEPAGE: str = "pages/cs/sys/portal/hisinoneStartPage.faces?page=1"
        LOGIN: str = "rds?state=user&type=1&category=auth.login"
        TIMETABLE: str = "pages/plan/individualTimetable.xhtml?_flowId=individualTimetableSchedule-flow"

    def __init__(self, fd_number: str, fd_password: str):
        self.__BASE_URL = "https://horstl.hs-fulda.de/qisserver/"
        self.__PAGE_IDS = self.PageIds
        self.fd_number = fd_number
        self.fd_password = fd_password
        self.__SESSION = self.__get_auth_session()

    # TODO Break method down
    def get_time_table(self) -> TimeTable:
        base_response_length = 8
        src = self.__get_time_table_src()
        soup = BeautifulSoup(src, "html.parser")
        days = soup.find_all("li", {"class": ["column", "bank_holiday"]})
        student = soup.find("h1", {"id": "hisinoneTitle"}).text.strip()
        time_period = soup.find("input", {"id": "plan:scheduleConfiguration:anzeigeoptionen:selectWeekInput"})["value"]

        time_table = TimeTable(student, time_period)

        for day_scrap, tt_day in zip(days, time_table.days.keys()):
            raw_date = day_scrap.text.\
                strip().\
                split(",")
            dow = raw_date[0]
            date = raw_date[1][1:11]

            current_day = Day(dow, date)
            time_table.days[tt_day] = current_day

            schedule = day_scrap.find_all("div", {"class": "schedulePanel"})
            for course in schedule:
                c = None
                raw_lines = course.text \
                    .replace("Status: ", "\n") \
                    .replace(" Durchführende Dozentinnen/Dozenten: ", "\n") \
                    .split("\n")
                if len(raw_lines) == base_response_length:
                    name = raw_lines[0].replace("\xa0", " ")
                    kind = raw_lines[1] \
                        .split(",")[0] \
                        .strip()
                    pg = raw_lines[1] \
                        .split(",")[1] \
                        .strip()
                    time = raw_lines[2]
                    frequency = raw_lines[3]
                    course_period = raw_lines[4]
                    room_info = raw_lines[5].replace("\xa0", " ")
                    docent = raw_lines[6]
                    status = raw_lines[7]
                    warning = "None"
                    c = Course(name, kind, pg, time, frequency, course_period, room_info, docent, status, warning)
                else:
                    warning = ""
                    for line in raw_lines[0:-7]:
                        if len(line) > 0:
                            warning += line + " "
                    name = raw_lines[-7].replace("\xa0", " ")
                    kind = raw_lines[-6] \
                        .split(",")[0] \
                        .strip()
                    pg = raw_lines[-6] \
                        .split(",")[1] \
                        .strip()
                    time = raw_lines[-5]
                    frequency = raw_lines[-4]
                    course_period = raw_lines[-3]
                    room_info = raw_lines[-2].replace("\xa0", " ")
                    docent = "No information available."
                    status = raw_lines[-1]
                    c = Course(name, kind, pg, time, frequency, course_period, room_info, docent, status, warning)
                current_day.add_course(c)
        return time_table

    def __get_time_table_src(self):
        s = self.__SESSION

        # TODO Find out how to retrieve weeks that aren't the current week
        # payload does noting at the moment
        # -----------------------------------------------------------------------------------------------------------
        # payload = {
        #     "plan:scheduleConfiguration:anzeigeoptionen:changeTerm": "45",
        #     "plan:scheduleConfiguration:anzeigeoptionen:changeTermInput": "Wintersemester 2019/20",
        #     "plan:scheduleConfiguration:anzeigeoptionen:auswahl_zeitraum": "woche",
        #     "plan:scheduleConfiguration:anzeigeoptionen:auswahl_zeitraumInput:": "Wochenauswahl",
        #     "plan:scheduleConfiguration:anzeigeoptionen:selectWeek": "45_2019",
        #    "plan:scheduleConfiguration:anzeigeoptionen:selectWeekInput:": "45. KW: 04.11.2019 - 10.11.2019",
        # }

        tt_url = self.__BASE_URL + self.__PAGE_IDS.TIMETABLE
        return s.get(tt_url).text

    def __get_auth_session(self):
        login_url = self.__BASE_URL + self.__PAGE_IDS.LOGIN

        payload = {
            "asdf": self.fd_number,
            "fdsa": self.fd_password,
        }

        session = requests.Session()

        session.post(login_url, payload)

        return session
