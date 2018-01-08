# -*- coding: utf-8 -*-
import datetime


def reformat_date(date):
    day = str(date.day) if str(date.day) == 2 else '0' + str(date.day)
    month = str(date.month) if str(date.month) == 2 else '0' + str(date.month)
    year = str(date.year)
    return day, month, year

class Flight(object):
    def __init__(self):
        self.leaving_time = None
        self.landing_time = None
        self.duration = None
        self.costs = []
        self.classes = []
        self.currency = None

    def __str__(self):
        class_cost = ''
        for i in range(len(self.costs)):
            class_cost += '\tclass: ' + self.classes[i] + ' cost: ' + self.costs[i] + ' ' + self.currency + '\n'
        return ('leaving time: {0} \n'
                'landing time: {1} \n'
                'duration: {2} \n'
                '**********\n'.format(self.leaving_time, self.landing_time, self.duration) +
                class_cost)


class Scraper(object):

    def __init__(self, host, dc, ac, date, return_date=None):
        self.headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      'Chrome/63.0.3239.84 Safari/537.36', 'Host': host}

        self.from_ = dc
        self.to = ac

        try:
            d = map(int, date.split('/'))
            self.date = datetime.date(d[2], d[1], d[0])
            self.day, self.month, self.year = reformat_date(self.date)
            today = datetime.date.today()
            if self.date <= today:
                raise ValueError
            if return_date:
                d = map(int, return_date.split('/'))
                self.return_date = datetime.date(d[2], d[1], d[0])
                self.rday, self.rmonth, self.ryear = reformat_date(self.return_date)
                if self.return_date < self.date:
                    raise ValueError
        except ValueError or TypeError:
                print 'некорректная дата'
                raise ValueError


    def change_ip(self):
        pass





#r = Scraper('secure.flydanaair.com', 'LOS', 'PHC', '16/01/2018', '18/01/2018')