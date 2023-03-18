import requests
from bs4 import BeautifulSoup
import pandas as pd

OUTPUT_FILE = 'clinics.csv'
TO_CSV = False
DISPLAY_DATA = True

URL_HEADER = 'https://www.gowabi.com'
URL = f'{URL_HEADER}/en/search?filter[search_text]=botox&page='


clinics = set()
clean_data = []

for i in range(1, 45):
    req = requests.get(URL+str(i))
    soup = BeautifulSoup(req.content, 'html.parser')
    divs = soup.find('div', {'class': 'providers_list_pagination'})
    if divs:
        headers = divs.find_all('h4')
        for header in headers:
            link = header.find('a')
            if link:
                url = link.get('href')
                clinics.add((header.text.strip(), URL_HEADER+str(url)))

for clinic in clinics:
    name, url = clinic
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    divs = soup.find_all('div', {'class': 'service-details-container'})
    if divs:
        for div in divs:
            service = div.find('strong')
            price = div.find('span', {'class': 'prices'})
            if service and price:
                row = [name, service.text.strip(), price.text.strip(), url]
                clean_data.append(row)

columns = ['Clinic', 'Service', 'Price', 'URL']
database = pd.DataFrame(clean_data, columns=columns)

if TO_CSV:
    database.to_csv(OUTPUT_FILE, index=False)

if DISPLAY_DATA:
    print(database)

if __name__ == '__main__':
    print('Done')
