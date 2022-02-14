from bs4 import BeautifulSoup
import requests

import constants as cons


class YnetMainPage():

    def __init__(self):
        self.main_url = cons.YNET_MAIN_PAGE_URL

    def scraping(self):
        html_test = requests.get(self.main_url)
        soup = BeautifulSoup(html_test.text, "lxml")
        jobs = soup.find_all("div", class_="slotView")
        for j in jobs:
            article = BeautifulSoup(str(j), "lxml")
            url = article.find("a").get("href")
            headline = article.find("a").text
            more_details = article.find("span", class_="dateView").text.replace(" ", "")
            split_date = more_details.split(",")
            # TODO: cast the date and time and insert into DB
