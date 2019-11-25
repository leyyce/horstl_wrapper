#!/usr/bin/env python3

from helpers.horstl_scrapper import HorstlScrapper
from helpers.mail_man import MailMan
from development.creds import FD_NUMBER, PASSWORD

if __name__ == '__main__':
    s = HorstlScrapper(FD_NUMBER, PASSWORD)
    tt = s.get_time_table()
    print(tt.to_string())
    # print(tt.days["monday"].to_string())
    # print(tt.days["monday"].courses[1].to_string())

    # mail_man = MailMan(FD_NUMBER, PASSWORD)

    # mail_man.print_home()
