#!/usr/bin/env python3
from imaplib import IMAP4_SSL
from getpass import getpass

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


def default():
    print("Welcome to the development script of horstl_wrapper!")
    success = False
    fd_num, password = None, None
    while not success:
        fd_num, password = _verify_login()
        if fd_num is not None:
            success = True
            print("Login successful!\n")
        else:
            print("Login failed. Try again:\n")

    task = ":pass"
    while len(task) != 0:
        task = (input("What do you want to do?\n\n\t1: Timetable\n\t2: Mail\n\tEnter to exit\n\n:> "))
        try:
            check = int(task)
        except ValueError:
            if len(task) == 0:
                break
            print("ERROR: Make sure to only enter numbers. Try again.")
            continue
        if check == 1:
            tt = HorstlScrapper(fd_num, password)
            print(str(tt.get_time_table()))
        elif check == 2:
            mail_man = MailMan(fd_num, password)
            mail_man.print_all_messages()
            mail_man.log_out()
        else:
            print(f"ERROR: Looks like the option {check} is not valid. Please try again.")


def _verify_login():
    fd_num = input("LOGIN:\n\nEnter your fd number [fdxxxxxx]: ")
    password = getpass("Enter your password: ")
    try:
        m = MailMan(fd_num, password)
    except IMAP4_SSL.error:
        return None, None
    return fd_num, password


if __name__ == '__main__':
    # time_table_test()
    # mail_test()
    default()
