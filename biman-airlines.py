import requests
import pickle
from lxml import etree


class Scraper(object):
    def __init__(self, host):
        self.headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/63.0.3239.84 Safari/537.36', 'Host': host}

    def change_ip(self):
        pass


class Biman(Scraper):

    def __init__(self, host, dc, ac, date, tt='OW', fl='on'):
        super(Biman, self).__init__(host)
        date = date.split('/')
        day = date[0]
        date_m = date[2] + '-' + date[1]
        self.flight = {'TT': tt,
                       'DC': dc,
                       'AC': ac,
                       'AM': date_m,
                       'AD': day,
                       'PA': '1',
                       'PC': '0',
                       'PI': '0',
                       'FL': fl,
                       'CD': ''}

    def make_request(self):
        return requests.get('https://flydanaair.com//process/', params=self.flight, headers=self.headers)


r = Biman('www.flydanaair.com', 'LOS', 'PHC', '16/01/2018')

content = r.make_request()