import requests
from bookingengine import Scraper, Flight
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

        self.headers['Referer'] = 'https://www.biman-airlines.com/'
        self.headers['X-Requested-With'] = "XMLHttpRequest"
        request = s.get('https://www.biman-airlines.com/shell.asp?get = bookings.css',
                        headers=self.headers,
                        verify=False)

        cookies = requests.utils.dict_from_cookiejar(request.cookies)
        print(cookies)
        print request.headers
        old_header = dict(self.headers)
        self.headers['X-Hash-Validate'] = "&".join([x[0] + "=" + x[1] for x in self.flight])

        request = s.head('https://www.biman-airlines.com/bookings/captcha.aspx',
                                 headers=self.headers,
                                 verify=False, cookies = cookies)
        #
        cookies.update({'chocolateChip':requests.utils.dict_from_cookiejar(request.cookies)['chocolateChip']})
        print(cookies)
        self.headers = old_header
        # #self.headers['Cookie'] = "BNI_bg_zapways=" + request.cookies['BNI_bg_zapways'] + \";chocolateChip=" + request.cookies['chocolateChip']
        print request.headers
        self.flight.append(('FS',request.headers['x-hash']))



        request = s.get('https://www.biman-airlines.com/bookings/flight_selection.aspx',
                               headers=self.headers,
                               params=self.flight,
                               verify=False,cookies = cookies)
        print request.status_code
        print request.headers
        #print s.cookies
        if request.status_code == '404':
            raise ValueError



        self.content = etree.HTML(request.content)

        '''text = open('biman_res_return.txt', 'r').read()
        self.content = etree.HTML(text)'''


# scr = Biman('www.biman-airlines.com', 'DAC', "KUL", "16/01/2018")
# scr.make_request()
# scr.combine_flights()