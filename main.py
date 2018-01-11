import warnings
import requests
from lxml.etree import HTML
import datetime
import biman
import flydanaair
from exceptions import *

warnings.filterwarnings("ignore")


def check_date(raw_date):

    d = map(int, raw_date.split('/'))
    if len(d) != 3:
        print 'Incorrect date format, try again'
        return None
    date = datetime.date(d[2], d[1], d[0])
    today = datetime.date.today()
    if date <= today:
        print 'This date has already passed, enter other date'
        return None
    return date


if __name__ == '__main__':

    site = ''
    while site != 'exit':

        print 'Input desire site (f - flydanaair, b - biman) or print exit to quit:'
        site = raw_input()

        if site == 'f':
            main_page = HTML(requests.get('http://www.flydanaair.com/', verify=False).content)
            available_airports = main_page.xpath(
                '//*[@id="first_section"]/div/select[@name="DC"]/option/@value'
            )[1:]
        elif site == 'b':
            main_page = HTML(requests.get('https://www.biman-airlines.com', verify=False).content)
            available_airports = main_page.xpath('//*[@name="DC"]/option/@value')[1:]

        while True:
            dep_city = raw_input('Departure city:\n')
            if dep_city not in available_airports:
                print 'You entered incorrect departure city, try again'
            else:
                break

        while True:
            dest_city = raw_input('Destination city:\n')
            if dest_city not in available_airports:
                print 'You entered incorrect destination city, try again'
            else:
                break

        while True:
            dep_date = raw_input('Departure date (DD/MM/YYYY):\n')
            dep_date = check_date(dep_date)
            if dep_date:
                break

        while True:
            ret_date = raw_input('Return date (if not needed, enter \'no\'):\n')
            if ret_date == 'no':
                ret_date = None
                break
            else:
                ret_date = check_date(ret_date)
                if ret_date:
                    if ret_date >= dep_date:
                        break

        try:
            if site == 'f':
                scr = flydanaair.Flydanaair(dep_city, dest_city, dep_date, ret_date)
            else:
                scr = biman.Biman(dep_city, dest_city, dep_date, ret_date)
            print 'Your results:\n'
            scr.make_request()
            scr.combine_flights()

        except ReferenceError:
            print 'There is no flights available for this date'
