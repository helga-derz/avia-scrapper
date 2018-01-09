import requests
from bookingengine import Scraper, Flight
from lxml import etree


class Flydanaair(Scraper):

    def __init__(self, host, dc, ac, date, return_date=None):
        super(Flydanaair, self).__init__(host, dc, ac, date, return_date)
        self.currency = 'NGN'
        self.content = ''

        if self.return_date:
            self.flight += [('RM', self.ryear + '-' + self.rmonth),
                            ('RD', self.rday)]

    def make_request(self):
        request = requests.get('https://secure.flydanaair.com/bookings/flight_selection.aspx',
                               params=self.flight,
                               headers=self.headers,
                               verify=False)
        #print request.status_code
        if request.status_code == '404':
            raise ValueError
        self.content = etree.HTML(request.content)

