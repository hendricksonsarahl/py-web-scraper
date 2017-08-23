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
trs = soup.find_all('tr')

# extract the data we want
for tr in trs:
    for link in tr.find_all('a'):
        fullLink = link.get ('href')

    tds = tr.find_all("td")
# use a "try" because the table is not well formatted. This allows the program to continue after encountering an error.
    try: 
# isolate the item by its column in the table and converts it into a string.
        years = str(tds[1].get_text())
        names = str(tds[0].get_text())
        positions = str(tds[2].get_text())
        parties = str(tds[3].get_text())
        states = str(tds[4].get_text())
        congress = tds[5].get_text()

    except:
        print "bad tr string"
        continue 

    writer.writerow([names, years, positions, parties, states, congress, fullLink])