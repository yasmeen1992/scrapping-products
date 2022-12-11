import requests
from bs4 import BeautifulSoup
import pandas  as pd
baseurl='https://www.thewhiskyexchange.com/'
headers={
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    
}
productlinks=[]
for x in range(1,4):
    r=requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}')
    soup=BeautifulSoup(r.content,'lxml')
    productlist=soup.find_all('li',class_='product-grid__item')
    for item in productlist:
        for link in item.find_all('a',href=True):
            productlinks.append(baseurl +link['href'])
wiskyList=[]
for link in productlinks:
        r=requests.get(link,headers=headers)
        if r.status_code==200:
            soup=BeautifulSoup(r.content,'lxml')
            try:
                name=soup.find('h1',class_='product-main__name').text.strip()
            except:
                name='no name'
            try:
                rating=soup.find('div',class_='review-overview').text.replace('\n','').replace(" ", "").strip()
            except:
                rating='no rating'
            try:
                price=soup.find('p',class_='product-action__price').text.strip()
            except:
               price='no price'
            wisky={
                'link':link,
                'name':name,
                'rating':rating,
                'price':price
            }
            wiskyList.append(wisky)
df=pd.DataFrame(wiskyList)
df.to_csv('thewhiskyexchange.csv', index=False,encoding='utf-8-sig')
