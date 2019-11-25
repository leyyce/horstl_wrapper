from dataclasses import dataclass
from requests import Session
from requests_html import HTML
from bs4 import BeautifulSoup

from helpers.base.scrapper import Scrapper

# [WIP] - THIS CLASS IS NOT FUNCTIONING


class MailMan(Scrapper):

    @dataclass
    class Pages:
        MAIL_HOME: str = None

    __PAGES = Pages
    __NJSCN = None

    def __init__(self, fd_number: str, fd_password: str):
        base_url = "https://webmail.hs-fulda.de/gw/webacc"
        super().__init__(fd_number, fd_password, base_url)
        self._set_session(self.__get_auth_session())

    def print_home(self):
        s = self._SESSION
        print(s.cookies)
        home = self._BASE_URL + self.Pages.MAIL_HOME
        # print(home)
        # self.__set_timezone()
        r = s.get(home)
        # print(r.content)

    def __set_timezone(self):
        s = self._SESSION
        url = f"https://webmail.hs-fulda.de/gw/webacc?User.context={self.__USER_CONTEXT}&action=Timezone.Update&merge=jerror&Timezone.Workstation.dstStartDate=2019-3-31T1:0&Timezone.Workstation.dstEndDate=2019-10-27T1:0&Timezone.Workstation.dstOffset=120&Timezone.Workstation.stdOffset=60&Timezone.Workstation.offsetAvailable=1&Timezone.Workstation.gmtOffset=60&Timezone.Workstation.HasDaylight=1&Timezone.Workstation.IsDaylight=0"
        s.get(url)

    def __get_auth_session(self):
        login_url = self._BASE_URL

        session = Session()

        r = session.get(login_url)

        # /home/yannic/.local/share/pyppeteer/local-chromium/575458
        html = HTML(html=r.content)
        html.render()

        print(html.search("Timezone.Workstation.dstStartDate"))

        soup = BeautifulSoup(html.html, "html.parser")

        print(soup.findAll(attrs={"name": "Timezone.Workstation.dstStartDate"}))
        self.__USER_CONTEXT = soup.find("input", {"name": "User.context"})["value"]
        tz_dst_start_date = soup.find("input", {"name": "Timezone.Workstation.dstStartDate"})["value"]
        tz_dst_end_date = soup.find("input", {"name": "Timezone.Workstation.dstEndDate"})["value"]
        tz_offset_available = soup.find("input", {"name": "Timezone.Workstation.offsetAvailable"})["value"]
        tz_gmt_offset = soup.find("input", {"name": "Timezone.Workstation.gmtOffset"})["value"]
        tz_has_daylight = soup.find("input", {"name": "Timezone.Workstation.HasDaylight"})["value"]
        tz_is_daylight = soup.find("input", {"name": "Timezone.Workstation.IsDaylight"})["value"]
        tz_std_offset = soup.find("input", {"name": "Timezone.Workstation.stdOffset"})["value"]
        tz_dst_offset = soup.find("input", {"name": "Timezone.Workstation.dstOffset"})["value"]

        payload = {
            "User.id": self.fd_number,
            "User.password": self.fd_password,
            "User.context": self.__USER_CONTEXT,
            "merge": "webaccx",
            "action": "User.login",
            "User.interface": "User.interface",
            "Timezone.Workstation.dstStartDate": tz_dst_start_date,
            "Timezone.Workstation.dstEndDate": tz_dst_end_date,
            "Timezone.Workstation.offsetAvailable": tz_offset_available,
            "Timezone.Workstation.gmtOffset": tz_gmt_offset,
            "Timezone.Workstation.HasDaylight": tz_has_daylight,
            "Timezone.Workstation.IsDaylight": tz_is_daylight,
            "Timezone.Workstation.stdOffset": tz_std_offset,
            "Timezone.Workstation.dstOffset": tz_dst_offset,
        }

        session.post(login_url, payload)
        print(self.__USER_CONTEXT)
        self.__PAGES.MAIL_HOME = f"?User.context={self.__USER_CONTEXT}&merge=jmsglist&Folder.queryCount=42&action=VMLFolder." \
                                f"Open&VMLFolder.refresh=true&Folder.id=7.DOM-STUD.PO-STUD2.100.0.1.0.1@16&Folder." \
                                f"type=Folder.UNIVERSAL&action=Categories.Get&Item.sendSids=true"
        return session
