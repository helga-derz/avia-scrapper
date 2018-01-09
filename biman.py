import requests
from bookingengine import Scraper, Flight
from lxml import etree


class Biman(Scraper):

    def __init__(self, host, dc, ac, date, return_date=None):
        super(Biman, self).__init__(host, dc, ac, date, return_date)
        self.currency = 'BDT'
        self.content = ''

        if self.return_date:
            self.flight.update({'RM': self.ryear + '-' + self.rmonth,
                                'RD': self.rday,
                                'CC': '',
                                'PT': ''})
        else:
            self.flight.update({'RM': self.year + '-' + self.month,
                                'RD': self.day,
                                'CC': '',
                                'PT': ''})

    def make_request(self):
        """
            Make request and save it as xml tree
        """
        s = requests.session()
        self.headers['Referer'] = 'https://www.biman-airlines.com/'
        old_header = dict(self.headers)
        self.headers['X-Hash-Validate'] = "&".join([x + "=" + self.flight[x] for x in self.flight])
        self.headers['X-Requested-With'] = "XMLHttpRequest"
        request = s.head('https://www.biman-airlines.com/bookings/captcha.aspx',
                                headers=self.headers,
                                verify=False)

        self.headers = old_header
        #self.headers['Cookie'] = "BNI_bg_zapways=" + request.cookies['BNI_bg_zapways'] + \";chocolateChip=" + request.cookies['chocolateChip']
        self.flight['FS'] = request.headers['X-Hash']

        request = s.get('https://www.biman-airlines.com/shell.asp?get = bookings.css',
                        headers=old_header,
                        verify=False)

        request = s.get('https://www.biman-airlines.com/bookings/flight_selection.aspx',
                               headers=old_header,
                               verify=False)
        print request.status_code
        if request.status_code == '404':
            raise ValueError



        self.content = etree.HTML(request.content)

        '''text = open('biman_res_return.txt', 'r').read()
        self.content = etree.HTML(text)'''
