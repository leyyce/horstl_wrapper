#!/usr/bin/env python3

from helpers.scrapper import Scrapper
from development.creds import FD_NUMBER, PASSWORD
from bs4 import BeautifulSoup

if __name__ == '__main__':
    s = Scrapper(FD_NUMBER, PASSWORD)
    soup = BeautifulSoup(s.get_time_table_src(), "html.parser")
    sP = soup.find_all("div", {"class": "schedulePanel"})
    time_period = soup.find("input", {"id": "plan:scheduleConfiguration:anzeigeoptionen:selectWeekInput"})["value"]
    student = soup.find("h1", {"id": "hisinoneTitle"}).text.strip()
    courses = []

    for course in sP:
        raw_lines = course.text\
            .replace("Status: ", "\n")\
            .replace(" Durchführende Dozentinnen/Dozenten: ", "\n")\
            .split("\n")

        kind = raw_lines[1]\
            .split(",")[0]\
            .strip()

        pg = raw_lines[1]\
            .split(",")[1]\
            .strip()

        courses.append({
            "Name": raw_lines[0].replace("\xa0", " "),
            "Typ": kind,
            "Parralelgruppe": pg,
            "Zeit": raw_lines[2],
            "Frequenz": raw_lines[3],
            "Zeitraum": raw_lines[4],
            "Rauminfo": raw_lines[5].replace("\xa0", " "),
            "Dozent/in": raw_lines[6],
            "Status": raw_lines[7]
        })

    print(f"\n{student}\n\nZeitraum - {time_period}\n")
    for course in courses:
        for key, value in course.items():
            print(f"{key}: {value}")
        print("\n")
