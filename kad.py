from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import datetime
import time
import random
import json
import argparse
import re

def validate(date_text):
    date_regex = re.compile(r"^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$")
    match = date_regex.search(date_text)
    if match:
        return True
    return False

parser = argparse.ArgumentParser()
parser.add_argument("-participant", dest="participant",default='')
parser.add_argument("-judge", dest="judge",default='')
parser.add_argument("-court", dest="court",default='')
parser.add_argument("-num", dest="numdelo",default='')
parser.add_argument("-datefrom", dest="datefrom",default='')
parser.add_argument("-dateto", dest="dateto",default='')
parser.add_argument("-file", dest="file",help='File to export data, default - data.json',default='data.json')
args = parser.parse_args()



playwright = sync_playwright().start()
browser = playwright.firefox.launch()
page = browser.new_page()
page.goto("https://kad.arbitr.ru")
time.sleep(2)
# Press Esc key to close information popup
page.keyboard.press("Escape")
time.sleep(2)
if args.participant:
    page.fill('textarea:visible',args.participant)
if args.judge:
    page.fill('input:visible',args.jugde)
if args.court:
    page.fill('input:visible >> nth=1',args.court)
if args.numdelo:
    page.fill('input:visible >> nth=2',args.numdelo)
if validate(args.datefrom) and validate(args.dateto):
    page.fill('input:visible >> nth=3',args.datefrom)
    page.fill('input:visible >> nth=4',args.dateto)
    page.keyboard.press("Tab")

time.sleep(1.2)
page.click('id=b-form-submit')
time.sleep(4)
#page.keyboard.press("Enter")

#page.screenshot(path="kad.png")

data = []

from bs4 import BeautifulSoup
souppage = BeautifulSoup(page.content(), 'lxml')
totalpages = souppage.find('input', id="documentsPagesCount").get('value')
#td = souppage.find('table', id="b-cases")
#soup = BeautifulSoup(td.prettify(), 'lxml')

#nums = soup.find_all('td', class_="num")
#tr = soup.find_all('tr')

for i in range(1,int(totalpages)+1):
    if i !=1:
        page.click(f'id=pages >> a[href = "#page{i}"]')
        time.sleep(random.random()*5+4)
    souppage = BeautifulSoup(page.content(), 'lxml')
    td = souppage.find('table', id="b-cases")
    soup = BeautifulSoup(td.prettify(), 'lxml')
    tr = soup.find_all('tr')
    for t in tr:
        delotype = t.find('td',class_='num').find('div',class_='b-container').find('div').get('class')[0]
        delo = ';'.join(t.find('td',class_='num').text.replace('\n', '').split())
        url = t.find('td',class_='num').find('a',class_='num_case').get('href')
        court = ';'.join(t.find('td',class_='court').text.replace('\n', '').split())
        try:
            plaintiff = t.find('td',class_='plaintiff').find('span',class_='js-rolloverHtml').text.split('\n')
            plaintiff = [i.strip() for i in plaintiff]
            plaintiff = ';'.join(list(filter(None,plaintiff)))
        except:
            plaintiff = ''
        try:
            respondent = []
            respall = t.find('td',class_='respondent').find_all('span',class_='js-rolloverHtml')
            for resp in respall:
                #respondent = t.find('td',class_='respondent').find('span',class_='js-rolloverHtml').text.split('\n')
                #respondent = [i.strip() for i in respondent]
                #respondent = ';'.join(list(filter(None,respondent)))
                resp = [i.strip() for i in resp.text.split('\n')]
                resp = ';'.join(list(filter(None,resp)))
                respondent.append(resp)
        except:
            respondent = ''
        data.append(
        {
            'тип_дела': delotype,
            'дело': delo,
            'url': url,
            'судья': court,
            'истец':plaintiff,
            'ответчик':respondent
        }
        )


with open(args.file,'w') as f:
    json.dump(data,f,ensure_ascii=False)
