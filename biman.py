import requests
from bookingengine import Scraper
from lxml.etree import HTML


class Biman(Scraper):

    def __init__(self, dc, ac, date, return_date=None):
        main_page = HTML(requests.get('https://www.biman-airlines.com', verify=False).content)
        available_airports = main_page.xpath('//*[@name="DC"]/option/@value')[1:]
        if dc not in available_airports or ac not in available_airports:
            raise ReferenceError
        self.host = 'www.biman-airlines.com'
        super(Biman, self).__init__(dc, ac, date, return_date)
        self.currency = 'BDT'
        self.content = ''

        if self.return_date:
            self.flight += [('RM', self.ryear + '-' + self.rmonth),
                            ('RD', self.rday),
                            ('CC', ''),
                            ('PT', '')]
        else:
            self.flight += [('RM', self.year + '-' + self.month),
                            ('RD', self.day),
                            ('CC', ''),
                            ('PT', '')]

    def make_request(self):
        """
            Make request and save it as xml tree
        """
        web_session = requests.Session()
        old_header = dict(self.headers)
        self.headers['X-Hash-Validate'] = "&".join([x[0] + "=" + x[1] for x in self.flight])

        request = web_session.head('https://www.biman-airlines.com/bookings/captcha.aspx',
                         headers=self.headers,
                         verify=False)

        self.headers = old_header
        self.flight.append(('FS', request.headers['x-hash']))

        request = web_session.get('https://www.biman-airlines.com/bookings/flight_selection.aspx',
                        headers=self.headers,
                        params=self.flight,
                        verify=False)

        self.content = HTML(request.content)
