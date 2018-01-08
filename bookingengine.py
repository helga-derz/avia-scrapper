# -*- coding: utf-8 -*-
import datetime

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
        landing_hour, landing_minute = map(int, self.landing_time.split(':'))
        leaving_hour, leaving_minute = map(int, self.leaving_time.split(':'))

        leaving = datetime.timedelta(hours=leaving_hour, minutes=leaving_minute)
        landing = datetime.timedelta(hours=landing_hour, minutes=landing_minute)

        if landing < leaving:
            self.duration = landing + (datetime.timedelta(hours=24,minutes=0) - leaving)
        else:
            self.duration = landing - leaving


    def __str__(self):


        if self.with_cost:
            class_cost = ''
            for i in range(len(self.costs)):
                class_cost += '\tclass: ' + self.classes[i] + ' cost: ' + self.costs[i] + ' ' + self.currency + '\n'
            return ('leaving time: {0} \n'
                        'landing time: {1} \n'
                        'duration: {2} \n'
                        '**********\n'.format(self.leaving_time, self.landing_time, self.duration) +
                        class_cost)
        else:
            return ('leaving time: {0} \n'
                        'landing time: {1} \n'
                        'duration: {2} \n'
                        .format(self.leaving_time, self.landing_time, self.duration))


class Scraper(object):

    def __init__(self, host, dc, ac, date, return_date=None):
        self.headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      'Chrome/63.0.3239.84 Safari/537.36', 'Host': host,'Upgrade-Insecure-Requests': '1',
                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                                     'Accept-Encoding': 'gzip, deflate, br',
                                     'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

        self.from_ = dc
        self.to = ac
        self.return_date = return_date

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

    def get_info(self, direction):
        pass

    def combine_flights(self):
        if not self.return_date:
            for flight in self.get_info('to'):
                print flight
        else:

            flights_to = self.get_info('to')
            flights_return = self.get_info('return')

            res = []

            for ft in flights_to:
                ft.with_cost = False
                info_ft = "To: \n" + str(ft)
                for fr in flights_return:
                    fr.with_cost = False
                    info_fr = "From: \n" + str(fr)
                    for i in range(len(ft.classes)):
                        for j in range(len(fr.classes)):
                            res.append((info_ft + 'class: ' + ft.classes[i] + ' cost: ' + ft.costs[i] + ' ' + ft.currency + '\n' + "\n" + info_fr + 'class: ' + fr.classes[j] + ' cost: ' + fr.costs[j] + ' ' + fr.currency + '\n', float(ft.costs[i].replace(",","")) + float(fr.costs[j].replace(",",""))))

            index = 1
            for flight in sorted(res, key = lambda x: x[1]):
                print "Combination N" + str(index)
                print flight[0] + "\n Final cost: " + str(flight[1]) +"\n"
                print "#############"
                index += 1






#r = Scraper('secure.flydanaair.com', 'LOS', 'PHC', '16/01/2018', '18/01/2018')