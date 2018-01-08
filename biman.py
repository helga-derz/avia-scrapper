import requests
from bookingengine import Scraper, Flight
from lxml import etree


class Biman(Scraper):

    def __init__(self, host, dc, ac, date, return_date=None):
        super(Biman, self).__init__(host, dc, ac, date, return_date)
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
                       'CD': '',
                       'CC': '',
                       'PT': ''}
        if self.return_date:
            self.flight.update({'RM': self.ryear + '-' + self.rmonth,
                                'RD': self.rday})
        else:
            self.flight.update({'RM': self.year + '-' + self.month,
                                'RD': self.day})

        self.make_request()
        self.combine_flights()


    def make_request(self):
        """
            Make request and save it as xml tree
        """
        self.headers['Referer'] = 'https://www.biman-airlines.com/'
        old_header = dict(self.headers)
        self.headers['X-Hash-Validate'] = "&".join([x + "=" + self.flight[x] for x in self.flight])
        self.headers['X-Requested-With'] = "XMLHttpRequest"
        request = requests.head('https://www.biman-airlines.com/bookings/captcha.aspx',
                                headers=self.headers,
                                verify=False)

        self.headers = old_header
        self.headers['Cookie'] = "BNI_bg_zapways=" + request.cookies['BNI_bg_zapways'] + \
                                 ";chocolateChip=" + request.cookies['chocolateChip']
        self.flight['FS'] = request.headers['X-Hash']

        request = requests.get('https://www.biman-airlines.com/bookings/flight_selection.aspx',
                               params=self.flight,
                               headers=self.headers,
                               verify=False)
        if request.status_code == '404':
            raise ValueError

        '''text = open('biman_res_return.txt', 'r').read()
        self.content = etree.HTML(text)'''

    def get_info(self, direction):
        flights = []
        trip_num = '2' if direction == 'return' else '1'
        classes = self.content.xpath(
            "//*[starts-with(@id, 'trip_" + trip_num + "') and contains(@class, "
                                                       "'requested-date')]/thead/tr/th/span/text()")
        tbody_node = self.content.xpath(
            "//*[starts-with(@id, 'trip_" + trip_num + "') and contains(@class, 'requested-date')]/tbody/tr")
        if not tbody_node:
            raise NotImplementedError
        else:
            for item in tbody_node:
                cur_fl = Flight()
                cur_fl.currency = 'BDT'
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
