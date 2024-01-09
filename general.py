import pygsheets
import requests
from bs4 import BeautifulSoup

# Extracting data
root = 'https://eldenring.wiki.fextralife.com'
url = '/Gestures'

r = requests.get(root + url)
soup = BeautifulSoup(r.content, 'html.parser')
rows = soup.select_one('.table-responsive')
rows = rows.select('tbody tr')

data = []
for itr in rows:
    field = itr.select_one('td')
    raw_data_list = field.select('a')
    if len(raw_data_list) == 0:
        raw_data = field
    else:
        raw_data = raw_data_list[0]
        if len(raw_data_list) > 1:
            raw_data = raw_data_list[1]
    name = raw_data.get_text()
    if len(raw_data_list) == 0:
        ref = ''
    else:
        ref = root + raw_data['href']
    data.append(['=HYPERLINK("' + ref + '","' + name + '")'])

# Writing data on Google Sheets

cred = "credentials.json"
client = pygsheets.authorize(service_account_file=cred)
spreadsht = client.open("DATA")
worksht = spreadsht.worksheet("title", "Sheet1")
worksht.update_values('A1:A' + str(len(data)), data)
