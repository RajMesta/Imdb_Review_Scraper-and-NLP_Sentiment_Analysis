import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver 
import time


def getmovies(m):
    URL = 'https://www.imdb.com/find?s=tt&q=' + m + '&ref_=nv_sr_sm'
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') 
    movies = soup.findAll('a', href=re.compile('^/title'))
    movies = movies[:4]
    urls = [re.search('"(.+?)"', str(text)).group(1) for text in movies[0::2]]  
    imgs = [re.search('src="(.+?)._', str(text)).group(1) for text in movies[0::2]]
    titles = [re.search('>(.+?)<', str(text)).group(1) for text in movies[1::2]]
    return urls,imgs,titles

def user_review(url,n):
    url = 'https://www.imdb.com/' + url + 'reviews?spoiler=hide&sort=helpfulnessScore&dir=asc&ratingFilter='+str(n)
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get(url)
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, 'html5lib') 
    t = soup.findAll('div',{"class":'header'})
    no = [re.search('an>(.+?) Re', str(text)).group(1) for text in t[0::2]]
    no[0] = no[0].replace(",","")
    no = int(no[0])
    no = no/25
    while True:
        try:
            if(no<1):
                break
            loadMoreButton = driver.find_element_by_xpath('//*[@id="load-more-trigger"]')
            loadMoreButton.click()
            no-=1
            time.sleep(4)
        except Exception as e:
            break
    page = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(page), 'html.parser')
    reviews = soup.findAll("div", {"class": "text show-more__control"})
    reviews = [str(r) for r in reviews]
    time.sleep(10)
    driver.quit()
    return reviews

def create_csv(urls,i,m):
    review_n = []
    review_p = []
    review_n += user_review(urls[i],1)+user_review(urls[i],2)+user_review(urls[i],3)+user_review(urls[i],4)
    review_p += user_review(urls[i],8)+user_review(urls[i],9)+user_review(urls[i],10)
    review = review_n + review_p
    rate = ['Negative']*len(review_n) + ['Positive']*len(review_p)
    df = pd.DataFrame(list(zip(review, rate)), columns =['Reviews', 'Sentiment']) 
    path = 'data/'+m+'.csv'
    df.to_csv(path) 