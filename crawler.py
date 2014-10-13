# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import csv
import codecs


url = 'http://www.uczsie.pl/korepetycje_z_jezyka_angielskiego.php'
patt = r'http://www\.uczsie\.pl/korepetycje_z_jezyka_angielskiego\.php\?szukano_id_wojewodztwa=[\w]&szukano_miejscowosc=[\w]'


def gether_urls(base, pattern):

    source_code = requests.get(base)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    for link in soup.findAll('a'):
        href = base + link.get('href')
        if re.match(pattern, href):
            yield href
        




def get_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text.replace("<br>", " ")
    soup = BeautifulSoup(plain_text, 'lxml' ,from_encoding='windows-1251') #windows-1251

    for contact in soup.findAll('td', {'class': 'tdSJkontakt'}):
        name = contact.b.string
        place = contact.previous_sibling.previous_sibling.b.string
        email = "not found"
        phone = "not found"

        for em in contact.findAll('a',{'class': 'mala_czcionka'}):
            ts = em['href'].encode('utf-8')
            if "mailto" in ts:
                email = em.string
                break
        for item in contact.contents:
            if 'Tel' in item:
                splitter = re.compile(r'\W');
                phone =  ''.join([i for i in splitter.split(item) if i.isdigit()])
                break
                     
        yield name.encode('latin-1'), email, phone, place.encode('latin-1')
        

    


f = csv.writer(open("uczsie_site.csv", "wb"))
f.writerow(["name", "email", "phone", "city"])

for u in gether_urls(url, patt):
    for (a, b, c, d) in get_data(u):
        f.writerow((a, b, c, d))


