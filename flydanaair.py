import requests
from bookingengine import Scraper
from lxml.etree import HTML

class Flydanaair(Scraper):

    def __init__(self, dc, ac, date, return_date=None):

        main_page = HTML(requests.get('http://www.flydanaair.com/', verify=False).content)
        available_airports = main_page.xpath('//*[@id="first_section"]/div/select[@name="DC"]/option/@value')[1:]
        if dc not in available_airports or ac not in available_airports:
            raise ReferenceError

        self.host = 'secure.flydanaair.com'
        super(Flydanaair, self).__init__(dc, ac, date, return_date)
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

        self.content = HTML(request.content)
