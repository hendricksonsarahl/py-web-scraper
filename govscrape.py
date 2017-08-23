import csv
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

# download the webpage via Requests
url = 'http://bioguide.congress.gov/biosearch/biosearch1.asp'
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

final_link = soup.p.a
final_link.decompose()

# convert extracted data to the proper encoding to read for every webpage scraped
http_encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(response.content, is_html=True)
encoding = html_encoding or http_encoding

# open csv writer before the loop starts
writer = csv.writer(open("./government.csv", "w"))
# write column headers as the first line
writer.writerow(["Name", "Years", "Position", "Party", "State", "Congress", "Link"]) 

# direct command to instruct BeautifulSoup to extract the exact HTML element we want
table = soup.find('tbody', attrs={'class': 'stripe'})

# extract the data we want and form it into a new list
list_of_rows = [] 
for row in table.findAll('a'):
    list_of_cells = []
    for cell in row.findAll('a'):
        text = cell.text.replace('&nbsp;', '')
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)

# create and hand to new csv file
writer.writerow(list_of_rows)