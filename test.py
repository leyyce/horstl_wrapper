#!/usr/bin/env python3
from getpass import getpass

from horstl_wrapper.helpers import HorstlScrapper
from horstl_wrapper.helpers import MailMan
from horstl_wrapper.development import FD_NUMBER, PASSWORD


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
    while True:
        fd_num = input("LOGIN:\n\nEnter your fd number [fdxxxxxx]: ")
        password = getpass("Enter your password: ")
        if _verify_login(fd_num, password):
            print("Login successful!\n")
            break
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
        else:
            print(f"ERROR: Looks like the option {check} is not valid. Please try again.")


def _verify_login(fd_number: str, password: str) -> bool:
    m = MailMan(fd_number, password)
    return m.logged_in


if __name__ == '__main__':
    # time_table_test()
    # mail_test()
    default()
