#!/usr/bin/env python3
from getpass import getpass

from horstl_wrapper.helpers import HorstlScrapper
from horstl_wrapper.helpers import MailMan
from horstl_wrapper.development import FD_NUMBER, PASSWORD


def time_table_test():
    horstl = HorstlScrapper(FD_NUMBER, PASSWORD)
    tt = horstl.get_time_table()
    print(tt)
    # print(tt.days.tuesday)
    # print(tt.days.monday.courses[1])


def mail_test():
    mail_man = MailMan(FD_NUMBER, PASSWORD)
    if mail_man.logged_in:
        messages = mail_man.get_all_messages()
        # messages = mail_man.get_unread_messages()
        # messages = mail_man.search_for_subject("Tans")
        # messages = mail_man.search_for_sender("Jetbrains")
        for m in messages:
            print(m)


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
        task = (input("MAIN MENU:\nWhat do you want to do?\n\n"
                      "\t1: Timetable\n"
                      "\t2: Mail\n"
                      "\tEnter to exit\n\n:> "))
        try:
            check = int(task)
        except ValueError:
            if len(task) == 0:
                break
            print("ERROR: Make sure to only enter numbers. Try again.")
            continue
        if check == 1:  # Case Timetable
            tt = HorstlScrapper(fd_num, password)
            print(tt.get_time_table())
        elif check == 2:  # Case mail
            mail_man = MailMan(fd_num, password)
            mail_task = ":pass"
            while len(mail_task) != 0:
                mail_task = (input("MAILS:\nWhat do you want to do?\n\n"
                                   "\t1: Show all mails\n\t2: Show new mails\n"
                                   "\t3: Search for subject\n"
                                   "\tEnter go back\n\n:> "))
                try:
                    mail_check = int(mail_task)
                except ValueError:
                    if len(mail_task) == 0:
                        break
                    print("ERROR: Make sure to only enter numbers. Try again.")
                    continue
                if mail_check == 1:  # Print all
                    messages = mail_man.get_all_messages()
                    for m in messages:
                        print(m)
                elif mail_check == 2:  # Print unread
                    messages = mail_man.get_unread_messages()
                    for m in messages:
                        print(m)
                elif mail_check == 3:  # Search subject
                    messages = mail_man.search_for_subject(input("Enter a search string: "))
                    if messages:
                        for m in messages:
                            print(m)
                    else:
                        print("Noting found.\n")
                else:
                    print(f"ERROR: Looks like the option {mail_check} is not valid. Please try again.")
        else:
            print(f"ERROR: Looks like the option {check} is not valid. Please try again.")


def _verify_login(fd_number: str, password: str) -> bool:
    m = MailMan(fd_number, password)
    return m.logged_in


if __name__ == '__main__':
    # time_table_test()
    # mail_test()
    default()
