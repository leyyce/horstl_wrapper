#!/usr/bin/env python3

from helpers.scrapper import Scrapper
from development.creds import FD_NUMBER, PASSWORD

if __name__ == '__main__':
    s = Scrapper(FD_NUMBER, PASSWORD)
    tt = s.get_time_table()

    print(tt.to_string())
