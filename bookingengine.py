import datetime
from my_exceptions import FlightsNotFound


def reformat_date(date):
    """
    Parsing date and adding '0' if day/month contains only one character.
    :param date: in datetime format
    """

    day = str(date.day) if len(str(date.day)) == 2 else '0' + str(date.day)
    month = str(date.month) if len(str(date.month)) == 2 else '0' + str(date.month)
    year = str(date.year)
    return day, month, year


class Flight(object):
    """
    Defining all flight details (leaving/landing time, cost etc).
    """

    def __init__(self):
        self.leaving_time = []
        self.landing_time = []
        self.duration = ''
        self.costs = []
        self.classes = []
        self.currency = None
        self.with_cost = True
        self.route = 'Nonstop'

    def calculate_duration(self):
        """
        Calculating the duration of a flight.
        """

        list_time = []
        for i in range(len(self.leaving_time)):
            if 'AM' in self.landing_time[i]:
                self.landing_time[i] = self.landing_time[i].replace(' AM', '')

            if 'AM' in self.leaving_time[i]:
                self.leaving_time[i] = self.leaving_time[i].replace(' AM', '')

            if 'PM' in self.landing_time[i]:
                self.landing_time[i] = self.landing_time[i].replace(' PM', '')
                t, m = self.landing_time[i].split(':')
                t = int(t) + 12
                self.landing_time[i] = str(t) + ':' + m

            if 'PM' in self.leaving_time[i]:
                self.leaving_time[i] = self.leaving_time[i].replace(' PM', '')
                t, m = self.leaving_time[i].split(':')
                t = int(t) + 12
                self.leaving_time[i] = str(t) + ':' + m

            landing_hour, landing_minute = map(int, self.landing_time[i].split(':'))
            leaving_hour, leaving_minute = map(int, self.leaving_time[i].split(':'))

            leaving = datetime.timedelta(hours=leaving_hour, minutes=leaving_minute)
            landing = datetime.timedelta(hours=landing_hour, minutes=landing_minute)
            list_time.append(leaving)
            list_time.append(landing)

        time_duration = datetime.timedelta(hours=0, minutes=0)

        for i in range(0, len(list_time) - 1, 2):
            leaving = list_time[i]
            landing = list_time[i + 1]

            if i != 0:

                landing_previous = list_time[i - 1]
                if leaving < landing_previous:
                    self.duration += ' + ' + str(
                            leaving + (datetime.timedelta(hours=24, minutes=0) - landing_previous)) + ' waiting + '
                    time_duration += leaving + (datetime.timedelta(hours=24, minutes=0) - landing_previous)
                else:
                    self.duration += ' + ' + str(leaving - landing_previous) + ' waiting + '
                    time_duration += leaving - landing_previous
            if landing < leaving:
                self.duration += str(landing + (datetime.timedelta(hours=24, minutes=0) - leaving)) + ' in air '
                time_duration += landing + (datetime.timedelta(hours=24, minutes=0) - leaving)
            else:
                self.duration += str(landing - leaving) + ' in air'
                time_duration += landing - leaving

        if len(self.leaving_time) > 1:
            self.duration += ' = ' + str(time_duration) + ' total'

    def __str__(self):
        if self.with_cost:
            class_cost = ''
            for i in range(len(self.costs)):
                if self.costs[i]:
                    class_cost += '\tclass: ' + self.classes[i] + ' cost: ' + \
                                  self.costs[i] + ' ' + self.currency + '\n'

            if self.route == 'Nonstop':
                return ('leaving time: {0} \n'
                        'landing time: {1} \n'
                        'route: {2} \n'
                        'duration: {3} \n'
                        '**********\n'.format(self.leaving_time, self.landing_time, self.route,
                                              self.duration) + class_cost)
            else:
                return ('route: {0} \n'
                        'duration: {1} \n'
                        '**********\n'.format(' -> '.join(
                        [self.route[i] + '(' + self.leaving_time[i] + '-' + self.landing_time[i] + ')' for i in
                         range(len(self.landing_time))]), self.duration) + class_cost
                        )

        if self.route == 'Nonstop':
            return ('leaving time: {0} \n'
                    'landing time: {1} \n'
                    'route: {2} \n'
                    'duration: {3} \n'
                    '**********\n'.format(self.leaving_time, self.landing_time, self.route,
                                          self.duration)
                    )
        else:
            return ('route: {0} \n'
                    'duration: {1} \n'
                    '**********\n'.format(' -> '.join(
                    [self.route[i] + '(' + self.leaving_time[i] + '-' + self.landing_time[i] + ')' for i in
                     range(len(self.landing_time))]), self.duration)
                    )


class Scraper(object):
    """
    The main handler of entered data.
    Provides all needed information from http response and then produce
    all possible combinations of flights.
    """

    def __init__(self, dc, ac, date, return_date):

        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML,'
                          ' like Gecko)Chrome/63.0.3239.84 Safari/537.36',
            'Host': self.host
        }

        self.from_ = dc
        self.to = ac
        self.date = date
        self.day, self.month, self.year = reformat_date(self.date)
        self.return_date = return_date
        if return_date:
            self.rday, self.rmonth, self.ryear = reformat_date(self.return_date)

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
        """
        Getting all needed flight details with x-path requests and creating a list of flights.
        """

        flights = []
        trip_num = '2' if direction == 'return' else '1'
        table_node = self.content.xpath(
                "//*[starts-with(@id, 'trip_{}') and contains(@class, 'requested-date')]".format(trip_num)
        )
        if not table_node:
            raise FlightsNotFound
        classes = table_node[0].xpath('.//thead/tr/th/span/text()')
        tbody_node = table_node[0].xpath('.//tbody')
        for item in tbody_node:
            flights_node = item.xpath('.//tr')

            if not flights_node:
                continue

            cur_fl = Flight()

            classes_node = item.xpath(".//*[starts-with(@class, 'family')]/label")
            for fl in classes_node:
                cost = fl.xpath(".//span/text()")
                if cost:
                    cur_fl.costs.append(cost[0])
                else:
                    cur_fl.costs.append(None)

            if not cur_fl.costs:
                continue

            cur_fl.leaving_time = item.xpath('.//tr/td[@class="time leaving"]/text()')
            cur_fl.landing_time = item.xpath('.//tr/td[@class="time landing"]/text()')
            cur_fl.classes = classes

            cur_fl.currency = self.content.xpath('*//span/b/text()')[0]

            cur_fl.calculate_duration()
            if len(flights_node) != 1:
                lt_route = item.xpath('.//tr/td[@class="route"]/span/text()')
                route = []
                for i in range(0, len(lt_route), 2):
                    route.append(lt_route[i] + '-' + lt_route[i + 1])
                cur_fl.route = list(route)
            flights.append(cur_fl)

        return flights

    def combine_flights(self):
        """
        Printing out all flights sorted by cost and create all possible combinations
        in case of return flight.
        """

        flights_to = self.get_info('to')

        if not flights_to:
            raise FlightsNotFound

        if not self.return_date:
            for flight in flights_to:
                print flight
        else:

            flights_return = self.get_info('return')

            if not flights_return:
                raise FlightsNotFound

            res = []

            for ft in flights_to:
                ft.with_cost = False
                info_ft = 'To: \n' + str(ft)
                for fr in flights_return:
                    fr.with_cost = False
                    info_fr = 'From: \n' + str(fr)
                    for i in range(len(ft.classes)):
                        if ft.costs[i]:
                            for j in range(len(fr.classes)):
                                if fr.costs[j]:
                                    res.append((info_ft + 'class: ' + ft.classes[i] + ' cost: ' + ft.costs[i] +
                                                ' ' + ft.currency + '\n' + '\n' + info_fr + 'class: ' + fr.classes[j] +
                                                ' cost: ' + fr.costs[j] + ' ' + fr.currency + '\n',
                                                float(ft.costs[i].replace(',', '')) +
                                                float(fr.costs[j].replace(',', ''))))

            index = 1
            for flight in sorted(res, key=lambda x: x[1]):
                print 'Combination N' + str(index)
                print flight[0] + '\n Final cost: ' + str(flight[1]) + '\n'
                print '#############'
                index += 1
