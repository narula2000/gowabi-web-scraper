import requests
from bs4 import BeautifulSoup
import pandas as pd

URL_HEADER = 'https://www.gowabi.com'
URL = f'{URL_HEADER}/en/search?filter[search_text]=botox&page='



clinics = set()
clean_data = []

for i in range(1, 45):
    req = requests.get(URL+str(i))
    soup = BeautifulSoup(req.content, 'html.parser')
    divs = soup.find(
        'div', {'class': 'providers_list_pagination infinit-scrol-box'})
    if divs:
        headers = divs.find_all('h4')

        for header in headers:
            link = header.find('a')
            if link:
                url = link.get('href')
                clinics.add((header.text.strip(), URL_HEADER+str(url)))
    break

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
                clean_data.append([name, service.text.strip(), price.text.strip(), url])


database = pd.DataFrame(clean_data, columns=['Clinic', 'Service', 'Price', 'URL'])
database.to_csv('clinics.csv', index=False)

if __name__ == '__main__':
    print(database)
    print('Done')