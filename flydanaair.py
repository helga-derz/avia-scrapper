import requests
from bookingengine import Scraper, Flight
from lxml import etree


class Flydanaair(Scraper):

    def __init__(self, host, dc, ac, date, return_date=None):
        super(Flydanaair, self).__init__(host, dc, ac, date, return_date)
        self.content = etree.HTML()
        self.flight = {'TT': 'RT' if self.return_date else 'OW',
                       'DC': dc,
                       'AC': ac,
                       'AM': self.year + '-' + self.month,
                       'AD': self.day,
                       'PA': '1',
                       'PC': '0',
                       'PI': '0',
                       'FL': 'on',
                       'CD': ''}
        if self.return_date:
            self.flight.update({'RM': self.ryear + '-' + self.rmonth,
                                'RD': self.rday})

        self.make_request()
        self.combine_flights()

    def make_request(self):
        request = requests.get('https://secure.flydanaair.com/bookings/flight_selection.aspx',
                               params=self.flight,
                               headers=self.headers,
                               verify=False)

        print request.status_code
        if request.status_code == '404':
            raise ValueError
        self.content = etree.HTML(request.content)

    def get_info(self, direction):
        flights = []
        trip_num = '2' if direction == 'return' else '1'
        classes = self.content.xpath("//*[starts-with(@id, 'trip_" + trip_num + "') and contains(@class, "
                                                                                "'requested-date')]/thead/tr/th/span"
                                                                                "/text()")
        tbody_node = self.content.xpath("//*[starts-with(@id, 'trip_" + trip_num + "') and contains(@class, "
                                                                                   "'requested-date')]/tbody/tr")
        if not tbody_node:
            raise NotImplementedError
        else:
            for item in tbody_node:
                cur_fl = Flight()
                cur_fl.currency = 'NGN'
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
                flights.append(cur_fl)
            return flights
