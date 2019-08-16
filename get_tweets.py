import os
import time
import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver #Download the webdriver mathching your browser at https://www.seleniumhq.org/download/

url = 'https://twitter.com/SarcasmMother' #Set the url of the twitter account
browser = webdriver.Firefox(executable_path=r'C:\Users\Alexandre\Desktop\test\geckodriver.exe') #Modify the path to match the location of the selenium webdriver modify the browser if needed (ex: Chrome, ...)
browser.get(url)

time.sleep(0.5)
SCROLL_PAUSE_TIME = 5 #the scrool down time needs to be change to allows all the items to load

last_height = browser.execute_script("return document.body.scrollHeight") #Get scroll height

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)") #Scroll down to bottom

    time.sleep(SCROLL_PAUSE_TIME) #Wait to load page

    new_height = browser.execute_script("return document.body.scrollHeight") #Calculate new scroll height and compare with last scroll height

    #If the new heigh equal the last heigh (meaning that we scroll the whole page then to to scrool)
    if new_height == last_height:
        break
    last_height = new_height

html_full_source = browser.page_source
browser.close()

soup = BeautifulSoup(html_full_source, features="html.parser")
now = time.strftime(' %d-%m-%Y %H-%M-%S')
csvFile = open(r'C:\Users\Alexandre\Desktop\test\tweet'+now+'.csv', 'a', newline='', encoding='utf-8')
csvWriter = csv.writer(csvFile, delimiter=';')
tweets= soup.find_all('div', {'class': 'content'})
headers = ['date','tweet']
csvWriter.writerow(headers)
data=[]
# extract the tweet and the date and write in a csv file
for item in tweets:
    item2 = item.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}, href=True)
    item3 = item.find('p', {'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'})
    if item2:
        date = item2.get('title')
        data.append(date.split('-')[1].strip())
    if item3:
        tweet = item3.get_text()
        data.append(tweet)

        for i in range(0, len(data)):
            data[i] = str(data[i]).replace(u'\xa0', '')
            data[i] = str(data[i]).replace(u'\n', '')
    csvWriter.writerow(data)
    data = []
