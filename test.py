#!/usr/bin/env python3

from helpers.horstl_scrapper import HorstlScrapper
from helpers.mail_man import MailMan
from development.creds import FD_NUMBER, PASSWORD


def time_table_test():
    horstl = HorstlScrapper(FD_NUMBER, PASSWORD)
    tt = horstl.get_time_table()
    # print(tt.to_string())
    # print(tt.days["tuesday"].to_string())
    print(tt.days.tuesday.to_string())
    print(tt.days.monday.courses[1].to_string())


def mail_test():
    mail_man = MailMan(FD_NUMBER, PASSWORD)
    mail_man.print_all_messages()


if __name__ == '__main__':
    time_table_test()
    # mail_test()
