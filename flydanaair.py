import requests
from lxml.etree import HTML
from bookingengine import Scraper


class Flydanaair(Scraper):
    """
    Define some additional information for request to www.flydanaair.com
    and provide the content of a response to http server.
    """

    def __init__(self, dc, ac, date, return_date=None):

        self.host = 'secure.flydanaair.com'
        super(Flydanaair, self).__init__(dc, ac, date, return_date)
        self.currency = 'NGN'
        self.content = ''

        if self.return_date:
            self.flight += [('RM', self.ryear + '-' + self.rmonth),
                            ('RD', self.rday)]

    def make_request(self):
        """
        Making a request and saving the response as xml tree.
        """

        request = requests.get('https://secure.flydanaair.com/bookings/flight_selection.aspx',
                               params=self.flight,
                               headers=self.headers,
                               verify=False)

        self.content = HTML(request.content)
