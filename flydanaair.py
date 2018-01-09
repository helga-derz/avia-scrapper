import requests
from bookingengine import Scraper, Flight
from lxml import etree


class Flydanaair(Scraper):

    def __init__(self, host, dc, ac, date, return_date=None):
        super(Flydanaair, self).__init__(host, dc, ac, date, return_date)
        self.currency = 'NGN'
        self.content = ''

        if self.return_date:
            self.flight.update({'RM': self.ryear + '-' + self.rmonth,
                                'RD': self.rday})

    def make_request(self):
        request = requests.get('https://secure.flydanaair.com/bookings/flight_selection.aspx',
                               params=self.flight,
                               headers=self.headers,
                               verify=False)
        #print request.status_code
        if request.status_code == '404':
            raise ValueError
        self.content = etree.HTML(request.content)

    '''def get_info(self, direction):
        flights = []
        trip_num = '2' if direction == 'return' else '1'
        table_node = self.content.xpath(
            "//*[starts-with(@id, 'trip_{0}') and contains(@class, 'requested-date')]".format(trip_num)
        )
        if not table_node:
            raise NotImplementedError
        classes = table_node[0].xpath(".//thead/tr/th/span/text()")
        tbody_node = table_node[0].xpath(".//tbody/tr")
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
            return flights'''
