import requests
from bookingengine import Scraper
from lxml import etree


class Biman(Scraper):

    def __init__(self, host, dc, ac, date, return_date=None):
        super(Biman, self).__init__(host, dc, ac, date, return_date)
        self.currency = 'BDT'
        self.content = ''

        if self.return_date:
            self.flight += [('RM', self.ryear + '-' + self.rmonth),
                            ('RD', self.rday),
                            ('CC', ''),
                            ('PT','')]
        else:
            self.flight += [('RM', self.year + '-' + self.month),
                            ('RD', self.day),
                            ('CC', ''),
                            ('PT', '')]

    def make_request(self):
        """
            Make request and save it as xml tree
        """
        s = requests.Session()
        old_header = dict(self.headers)
        self.headers['X-Hash-Validate'] = "&".join([x[0] + "=" + x[1] for x in self.flight])

        request = s.head('https://www.biman-airlines.com/bookings/captcha.aspx',
                         headers=self.headers,
                         verify=False)

        self.headers = old_header
        self.flight.append(('FS',request.headers['x-hash']))

        request = s.get('https://www.biman-airlines.com/bookings/flight_selection.aspx',
                        headers=self.headers,
                        params=self.flight,
                        verify=False)

        if request.status_code == '404':
            raise ValueError

        self.content = etree.HTML(request.content)
