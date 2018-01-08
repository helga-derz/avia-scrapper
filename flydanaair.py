import requests
from bookingengine import Scraper, Flight
from lxml import etree
import pickle

class Flydanaair(Scraper):

    def __init__(self, host, dc, ac, date, tt='OW', fl='on', return_date=''):
        super(Flydanaair, self).__init__(host, dc, ac, date, return_date)

        self.flight = {'TT': tt,
                       'DC': dc,
                       'AC': ac,
                       'AM': self.year + '-' + self.month,
                       'AD': self.day,
                       'PA': '1',
                       'PC': '0',
                       'PI': '0',
                       'FL': fl,
                       'CD': ''}

    def make_request(self):
        '''request = requests.get('https://secure.flydanaair.com/bookings/flight_selection.aspx',
                               params=self.flight,
                               headers=self.headers,
                               verify=False)'''
        #self.content = etree.HTML(request.content)

        text = open('res_text.pkl', 'r')
        text = pickle.load(text)

        self.content = etree.HTML(text)

    def get_info(self):
        flights = []
        tbody_node = self.content.xpath('//*[@id="trip_1_date_' + self.year + '_' + self.month + '_' + self.day + '"]/tbody/tr')
        if not tbody_node:
            return -1
        else:
            for item in tbody_node:
                cur_fl = Flight()
                cur_fl.currency = 'NGN'
                cur_fl.leaving_time = item.xpath('.//td[@class="time leaving"]/text()')
                cur_fl.landing_time = item.xpath('.//td[@class="time landing"]/text()')
                cur_fl.duration = 'DURATION'
                cur_fl.costs = item.xpath(".//*[starts-with(@class, 'family')]/label/span/text()")
                cur_fl.classes = item.xpath(".//*[starts-with(@class, 'family')]/@class")
                flights.append(cur_fl)
            return flights


r = Flydanaair('secure.flydanaair.com', 'LOS', 'PHC', '16/01/2018')

content = r.make_request()
info = r.get_info()
for i in info:
    print i

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
