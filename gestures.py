import pygsheets
import requests
from bs4 import BeautifulSoup

# Extracting data
root = 'https://eldenring.wiki.fextralife.com'
url = '/Gestures'

r = requests.get(root + url)
soup = BeautifulSoup(r.content, 'html.parser')
rows = soup.select('#wiki-content-block .row')

data = []
for row in rows:
    boxes = row.select('.col-xs-6')
    for itr_1 in boxes:
        box_name = itr_1.select('h4')
        if len(box_name) == 0:
            break
        name = box_name[0].get_text()
        print(name)
        data.append([name])
# Writing data on Google Sheets

cred = "credentials.json"
client = pygsheets.authorize(service_account_file=cred)
spreadsht = client.open("DATA")
worksht = spreadsht.worksheet("title", "Sheet1")
worksht.update_values('A1:A' + str(len(data)), data)
