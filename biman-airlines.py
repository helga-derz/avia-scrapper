import requests
from bookingengine import Scraper, Flight
from lxml import etree
import datetime
import pickle

import urllib2


class Biman(Scraper):

    def __init__(self, host, dc, ac, date, return_date=None, tt='OW', fl='on'):
        super(Biman, self).__init__(host, dc, ac, date, return_date)

        self.flight = {'TT': 'RT' if self.return_date else tt,
                       'DC': dc,
                       'AC': ac,
                       'AM': self.year + '-' + self.month,
                       'AD': self.day,
                       'PA': '1',
                       'PC': '0',
                       'PI': '0',
                       'FL': fl,
                       'CD': '',
                       'CC': '',
                       'PT': ''}
        if self.return_date:
            self.flight.update({'RM': self.ryear + '-' + self.rmonth,
                                'RD': self.rday})
        else:
            self.flight.update({'RM': self.year + '-' + self.month,
                                'RD': self.day})

    def make_request(self):
        self.headers['Referer'] = 'https://www.biman-airlines.com/'
        old_header = dict(self.headers)
        self.headers['X-Hash-Validate'] = "&".join([x +"=" + self.flight[x] for x in self.flight])
        self.headers['X-Requested-With'] = "XMLHttpRequest"
        request = requests.head('https://www.biman-airlines.com/bookings/captcha.aspx',
                               headers=self.headers,
                               verify=False)

        self.headers = old_header
        self.headers['Cookie'] =  "BNI_bg_zapways="+request.cookies['BNI_bg_zapways'] + ";chocolateChip=" + request.cookies['chocolateChip']
        self.flight['FS'] =request.headers['X-Hash']
        #self.headers.pop('X-Hash-Validate')
        print request.status_code
        print request.headers

        request = requests.get('https://www.biman-airlines.com/bookings/flight_selection.aspx',
                               params=self.flight,
                               headers=self.headers,
                               verify=False)
        print request.status_code
        print request.headers
        self.content = etree.HTML(request.content)


        out2 = open('res_text_biman.pkl', 'wb')
        pickle.dump(request.text, out2)
        out2.close()

        '''text = open('res_text.pkl', 'r')
        text = pickle.load(text)

        self.content = etree.HTML(text)'''

    def get_info(self, direction):
        flights = []
        trip_num = '2' if direction == 'return' else '1'
        classes = self.content.xpath("//*[starts-with(@id, 'trip_"+ trip_num + "') and contains(@class, 'requested-date')]/thead/tr/th/span/text()")
        tbody_node = self.content.xpath("//*[starts-with(@id, 'trip_"+ trip_num + "') and contains(@class, 'requested-date')]/tbody/tr") #_date_' + self.year + '_' + self.month + '_' + self.day + '"]/tbody/tr')
        if not tbody_node:
            return -1
        else:
            for item in tbody_node:
                cur_fl = Flight()
                cur_fl.currency = 'NGN'
                cur_fl.leaving_time = item.xpath('.//td[@class="time leaving"]/text()')[0]
                cur_fl.landing_time = item.xpath('.//td[@class="time landing"]/text()')[0]
                cur_fl.calculate_duration()
                cur_fl.costs = item.xpath(".//*[starts-with(@class, 'family')]/label/span/text()")
                cur_fl.classes = classes                            #.//*[starts-with(@class, 'family')]/@class")
                flights.append(cur_fl)
            return flights


r = Biman('www.biman-airlines.com', 'DAC', 'KUL', '10/01/2018')

content = r.make_request()
#info = r.get_info('return')
#for i in info:
#    print i
r.combine_flights()

'''out1 = open('res_cont.pkl', 'wb')
pickle.dump(content.content, out1)

out2 = open('res_text.pkl', 'wb')
pickle.dump(content.text, out2)

content = r.make_request()

print content.text

out1 = open('res_cont.pkl', 'wb')
pickle.dump(content.content, out1)

out2 = open('res_text.pkl', 'wb')
pickle.dump(content.text, out2)'''

# tree = etree.HTML(r.text)
# form_node = tree.xpath("//form[@method='post']")

# print len(form_node)


'''GET /bookings/flight_selection.aspx?TT=OW&DC=LOS&AC=PHC&AM=2018-01&AD=16&PA=1&PC=0&PI=0&FL=on&CD= HTTP/1.1
GET /bookings/flight_selection.aspx?TT=OW&DC=LOS&AC=PHC&AM=-&AD=&PA=1&PC=0&PI=0&FL=on&CD= HTTP/1.1'''
