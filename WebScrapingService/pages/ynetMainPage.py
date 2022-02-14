from bs4 import BeautifulSoup
import requests

import constants as cons


def scraping():
        html_test = requests.get(cons.YNET_MAIN_PAGE_URL)
        soup = BeautifulSoup(html_test.text, "lxml")
        jobs = soup.find_all("div", class_="slotView")
        for j in jobs:
            article = BeautifulSoup(str(j), "lxml")
            url = article.find("a").get("href")
            headline = article.find("a").text
            more_details = article.find("span", class_="dateView").text.replace(" ", "")
            split_date = more_details.split(",")
            print(split_date)
            # TODO: cast the date and time and insert into DB
