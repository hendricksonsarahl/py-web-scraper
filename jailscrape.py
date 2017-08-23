import csv
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

# download the webpage via Requests
url = 'http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp'
response = requests.get(url)

# convert extracted data to the proper encoding to read for every webpage scraped
http_encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(response.content, is_html=True)
encoding = html_encoding or http_encoding

soup = BeautifulSoup(response.content, "html.parser")

# open csv writer before the loop starts
writer = csv.writer(open("./inmates.csv", "wb"))


# direct command to instruct BeautifulSoup to extract the exact HTML element we want
table = soup.find('tbody', attrs={'class': 'stripe'})

# extract the data we want and form it into a new list
list_of_rows = [] 
for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace('&nbsp;', '')
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)

# create and hand to new csv file
writer.writerow(list_of_rows)