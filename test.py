from lxml import etree
import pickle

'''cont = open('res_cont.pkl', 'r')
cont = pickle.load(cont)'''
text = open('res_text.pkl', 'r')
text = pickle.load(text)




tree = etree.HTML(text)
tbody_node = tree.xpath('//*[@id="trip_1_date_2018_01_16"]/tbody/tr')

leav_time = []
n= []

for i in tbody_node:

    leav_time.append(i.xpath(".//*[starts-with(@class, 'family')]/label/span/text()"))
    n.append(i.xpath(".//*[starts-with(@class, 'family')]/@class"))

print leav_time
print n