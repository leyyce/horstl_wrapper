from requests import Session
from bs4 import BeautifulSoup

from horstl_wrapper.helpers.base import Scrapper
from horstl_wrapper.models import Day
from horstl_wrapper.models import Course
from horstl_wrapper.models import TimeTable
from enum import Enum


class HorstlScrapper(Scrapper):

    class Pages(Enum):
        HOMEPAGE = "pages/cs/sys/portal/hisinoneStartPage.faces?page=1"
        LOGIN = "rds?state=user&type=1&category=auth.login"
        TIMETABLE = "pages/plan/individualTimetable.xhtml?_flowId=individualTimetableSchedule-flow"

    def __init__(self, fd_number: str, fd_password: str):
        base_url = "https://horstl.hs-fulda.de/qisserver/"
        super().__init__(fd_number, fd_password, base_url)
        self._set_session(self.__get_auth_session())

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
                    ident = raw_lines[0].split("\xa0")[0]
                    name = raw_lines[0].split("\xa0")[1]
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
                    c = Course(ident, name, kind, pg, time, frequency, course_period, room_info, docent, status,
                               warning)
                else:
                    warning = ""
                    for line in raw_lines[0:-7]:
                        if len(line) > 0:
                            warning += line + " "
                    ident = raw_lines[-7].split("\xa0")[0]
                    name = raw_lines[-7].split("\xa0")[1]
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
                    c = Course(ident, name, kind, pg, time, frequency, course_period, room_info, docent, status, warning)
                current_day.add_course(c)
        return time_table

    def __get_time_table_src(self):
        s = self._SESSION

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
        tt_url = f"{self._BASE_URL}{HorstlScrapper.Pages.TIMETABLE.value}"
        return s.get(tt_url).text

    def __get_auth_session(self):
        login_url = f"{self._BASE_URL}{HorstlScrapper.Pages.LOGIN.value}"

        payload = {
            "asdf": self.fd_number,
            "fdsa": self.fd_password,
        }

        session = Session()

        session.post(login_url, payload)

        return session
