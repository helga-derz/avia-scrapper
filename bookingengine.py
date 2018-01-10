# -*- coding: utf-8 -*-
import datetime
from exceptions import *


def reformat_date(date):
    day = str(date.day) if len(str(date.day)) == 2 else '0' + str(date.day)
    month = str(date.month) if len(str(date.month)) == 2 else '0' + str(date.month)
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
        self.with_cost = True

    def calculate_duration(self):

        if "AM" in self.landing_time:
            self.landing_time = self.landing_time.replace(" AM", "")

        if "AM" in self.leaving_time:
            self.leaving_time = self.leaving_time.replace(" AM", "")

        if "PM" in self.landing_time:
            self.landing_time = self.landing_time.replace(" PM", "")
            t, m = self.landing_time.split(":")
            t = int(t) + 12
            self.landing_time = str(t) + ":" + m

        if "PM" in self.leaving_time:
            self.leaving_time = self.leaving_time.replace(" PM", "")
            t, m = self.leaving_time.split(":")
            t = int(t) + 12
            self.leaving_time = str(t) + ":" + m

        landing_hour, landing_minute = map(int, self.landing_time.split(':'))
        leaving_hour, leaving_minute = map(int, self.leaving_time.split(':'))

        leaving = datetime.timedelta(hours=leaving_hour, minutes=leaving_minute)
        landing = datetime.timedelta(hours=landing_hour, minutes=landing_minute)

        if landing < leaving:
            self.duration = landing + (datetime.timedelta(hours=24, minutes=0) - leaving)
        else:
            self.duration = landing - leaving

    def __str__(self):
        if self.with_cost:
            class_cost = ''
            for i in range(len(self.costs)):
                if self.costs[i]:
                    class_cost += '\tclass: ' + self.classes[i] + ' cost: ' + \
                                  self.costs[i] + ' ' + self.currency + '\n'
            return ('leaving time: {0} \n'
                    'landing time: {1} \n'
                    'duration: {2} \n'
                    '**********\n'.format(self.leaving_time, self.landing_time, self.duration) +
                    class_cost)
        return ('leaving time: {0} \n'
                'landing time: {1} \n'
                'duration: {2} \n'.format(self.leaving_time, self.landing_time, self.duration))


class Scraper(object):

    def __init__(self, dc, ac, date, return_date=None):
        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML,'
                          ' like Gecko)Chrome/63.0.3239.84 Safari/537.36',
            'Host': self.host
        }

        self.from_ = dc
        self.to = ac
        self.return_date = return_date

        try:
            d = map(int, date.split('/'))
            if len(d) != 3:
                raise IncorrectDate
            self.date = datetime.date(d[2], d[1], d[0])
            self.day, self.month, self.year = reformat_date(self.date)
            today = datetime.date.today()
            if self.date <= today:
                raise ValueError
            if return_date:
                d = map(int, return_date.split('/'))
                if len(d) != 3:
                    raise ValueError
                self.return_date = datetime.date(d[2], d[1], d[0])
                self.rday, self.rmonth, self.ryear = reformat_date(self.return_date)
                if self.return_date < self.date:
                    raise ValueError

        except ValueError or TypeError:
            print 'incorrect date'
            raise ValueError

        self.flight = [
            ('TT', 'RT' if self.return_date else 'OW'),
            ('DC', dc),
            ('AC', ac),
            ('AM', self.year + '-' + self.month),
            ('AD', self.day),
            ('PA', '1'),
            ('PC', '0'),
            ('PI', '0'),
            ('FL', 'on'),
            ('CD', '')
            ]

    def get_info(self, direction):
        flights = []
        trip_num = '2' if direction == 'return' else '1'
        table_node = self.content.xpath(
            "//*[starts-with(@id, 'trip_{}') and contains(@class, 'requested-date')]".format(trip_num)
        )
        if not table_node:
            raise FlightsNotFound
        classes = table_node[0].xpath(".//thead/tr/th/span/text()")
        tbody_node = table_node[0].xpath(".//tbody/tr")
        for item in tbody_node:
            cur_fl = Flight()
            cur_fl.currency = self.currency
            cur_fl.leaving_time = item.xpath('.//td[@class="time leaving"]/text()')[0]
            cur_fl.landing_time = item.xpath('.//td[@class="time landing"]/text()')[0]
            cur_fl.calculate_duration()
            classes_node = item.xpath(".//*[starts-with(@class, 'family')]/label")
            for fl in classes_node:
                cost = fl.xpath(".//span/text()")
                if cost:
                    cur_fl.costs.append(cost[0])
                else:
                    cur_fl.costs.append(None)
            cur_fl.classes = classes

            if cur_fl.costs:
                flights.append(cur_fl)

        return flights

    def combine_flights(self):
        flights_to = self.get_info('to')

        if not self.return_date:
            for flight in flights_to:
                print flight
        else:

            flights_return = self.get_info('return')

            res = []

            for ft in flights_to:
                ft.with_cost = False
                info_ft = "To: \n" + str(ft)
                for fr in flights_return:
                    fr.with_cost = False
                    info_fr = "From: \n" + str(fr)
                    for i in range(len(ft.classes)):
                        if ft.costs[i]:
                            for j in range(len(fr.classes)):
                                if fr.costs[j]:
                                    res.append((info_ft + 'class: ' + ft.classes[i] + ' cost: ' + ft.costs[i] +
                                                ' ' + ft.currency + '\n' + "\n" + info_fr + 'class: ' + fr.classes[j] +
                                                ' cost: ' + fr.costs[j] + ' ' + fr.currency + '\n',
                                                float(ft.costs[i].replace(",", "")) +
                                                float(fr.costs[j].replace(",", ""))))

            index = 1
            for flight in sorted(res, key=lambda x: x[1]):
                print "Combination N" + str(index)
                print flight[0] + "\n Final cost: " + str(flight[1]) + "\n"
                print "#############"
                index += 1
