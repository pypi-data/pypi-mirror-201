import requests
from bs4 import BeautifulSoup
import fake_useragent
from time import sleep

url = 'https://www.minusrus.com/'

user = fake_useragent.UserAgent().random

headers = {
    'User-Agent': user
}

response = requests.get(url, headers=headers)

bs = BeautifulSoup(response.text, 'html.parser')

personnel = bs.find('div', class_ = 'card__amount').text.replace('~', '').strip()

died_personnel = bs.find_all('div', class_ = 'amount-details__item')[0].text.replace('~', '').replace('вбито', '').strip()
wounded_personnel = bs.find_all('div', class_ = 'amount-details__item')[1].text.replace('~', '').replace('поранено', '').strip()
captured_personnel = bs.find_all('div', class_ = 'amount-details__item')[2].text.replace('~', '').replace('взято в полон', '').strip()

if '+' not in personnel:
    total_personnel = bs.find_all('div', class_ = 'card__amount')[0].find_all('span')[0].text.replace('~', '').strip()
    total_personnel_quantity = ''
else:
    total_personnel = bs.find_all('div', class_ = 'card__amount')[0].find_all('span')[0].text.replace('~', '').strip()
    total_personnel_quantity = bs.find_all('div', class_ = 'card__amount')[0].find_all('span')[1].text.strip()


bbm = bs.find_all('div', class_ = 'card__amount')[1].text.replace('~', '').strip()
if '+' not in bbm:
    bbm = bs.find_all('div', class_ = 'card__amount')[0].find_all('span')[0].text.replace('~', '').strip()
    bbm_quantity = ''
else:
    bbm = bs.find_all('div', class_ = 'card__amount')[1].find_all('span')[0].text.replace('~', '').strip()
    bbm_quantity = bs.find_all('div', class_ = 'card__amount')[1].find_all('span')[1].text.strip()


tanks = bs.find_all('div', class_ = 'card__amount')[2].text
if '+' not in tanks:
    tanks = bs.find_all('div', class_ = 'card__amount')[2].find_all('span')[0].text.replace('~', '').strip()
    tanks_quantity = ''
else:
    tanks = bs.find_all('div', class_ = 'card__amount')[2].find_all('span')[0].text.replace('~', '').strip()
    tanks_quantity = bs.find_all('div', class_ = 'card__amount')[2].find_all('span')[1].text.strip()
        
    
artillery = bs.find_all('div', class_ = 'card__amount')[3].text.strip()
if '+' not in artillery:
    artillery = bs.find_all('div', class_ = 'card__amount')[3].find_all('span')[0].text.replace('~', '').strip()
    artillery_quantity = ''
else:
    artillery = bs.find_all('div', class_ = 'card__amount')[3].find_all('span')[0].text.replace('~', '').strip()
    artillery_quantity = bs.find_all('div', class_ = 'card__amount')[3].find_all('span')[1].text.strip()


planes = bs.find_all('div', class_ = 'card__amount')[4].text
if '+' not in planes:
    planes = bs.find_all('div', class_ = 'card__amount')[4].find_all('span')[0].text.replace('~', '').strip()
    planes_quantity = ''
else:
    planes = bs.find_all('div', class_ = 'card__amount')[4].find_all('span')[0].text.replace('~', '').strip()
    planes_quantity = bs.find_all('div', class_ = 'card__amount')[4].find_all('span')[1].text.strip()


helicopters = bs.find_all('div', class_ = 'card__amount')[5].text.replace('~', '').strip()
if '+' not in helicopters:
    helicopters = bs.find_all('div', class_ = 'card__amount')[4].find_all('span')[0].text.replace('~', '').strip()
    helicopters_quantity = ''
else:
    helicopters = bs.find_all('div', class_ = 'card__amount')[5].find_all('span')[0].text.replace('~', '').strip()
    helicopters_quantity = bs.find_all('div', class_ = 'card__amount')[5].find_all('span')[1].text.strip()


warships = bs.find_all('div', class_ = 'card__amount')[6].text.replace('~', '').strip()
if '+' not in warships:
    warships = bs.find_all('div', class_ = 'card__amount')[6].find_all('span')[0].text.replace('~', '').strip()
    warships_quantity = ''
else:
    warships = bs.find_all('div', class_ = 'card__amount')[6].find_all('span')[0].text.replace('~', '').strip()
    warships_quantity = bs.find_all('div', class_ = 'card__amount')[6].find_all('span')[1].text.strip()