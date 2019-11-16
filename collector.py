from bs4 import BeautifulSoup
import os
import requests
import time
import random

# this lines create a new directory, Movies, in your project folder
if not os.path.exists("Movies\\"):
    os.makedirs("Movies\\")

url = "https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html"
# you should change this number
page = requests.get(url)
data = page.text
soup = BeautifulSoup(data)

counter = 0
for link in soup.find_all('a'):
    time.sleep(random.randint(1, 6))  # waiting a variable amount of seconds for don't be catched by Wikipedia

    localurl = link.get('href')
    r = requests.get(localurl)  # fetching the html page

    with open("Movies\\movie" + str(counter) + ".html", 'wb') as f:  # creating a new file in the Movies folder
        f.write(r.content)  # put in this new file the html page of the movie

    counter += 1  # starting form 0 each different movie will take a different index