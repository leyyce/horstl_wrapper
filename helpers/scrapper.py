from dataclasses import dataclass
import requests


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

    def get_time_table_src(self):
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
