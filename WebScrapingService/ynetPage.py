from datetime import datetime

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

import constants as cons
from DataBaseService.models.models import NewsArticles
import re

from WebScrapingService import dbFunctions


def update_ynet_news():
    html_test = requests.get(cons.YNET_MAIN_PAGE_URL)
    soup = BeautifulSoup(html_test.text, "lxml")
    jobs = soup.find_all("div", class_="slotView")
    ynet_last_update = dbFunctions.last_update_by_page(cons.YNET_PAGE_CODE)
    for j in tqdm(jobs):
        article = BeautifulSoup(str(j), "lxml")
        date_time = get_format_datetime_from_ynet(article.find("span", class_="dateView").text.replace(" ", ""))
        if ynet_last_update and ynet_last_update.date_time > date_time:
            break
        url = article.find("a").get("href")
        head_line = article.find("a").text
        if dbFunctions.does_headline_exist(head_line):
            continue
        category = get_news_category(url)
        dbFunctions.insert_news(NewsArticles(url=url, head_line=head_line, date_time=date_time, cat_id=category,
                                             page_code=cons.YNET_PAGE_CODE))


def get_format_datetime_from_ynet(details):
    split_date = details.split(",")
    time = split_date[0]
    date = split_date[1]
    clear_datetime = date + ";" + time
    return datetime.strptime(clear_datetime, cons.YNET_DATE_TIME_FORMAT)


def get_news_category(url: str):
    html_test = requests.get(url)
    soup = BeautifulSoup(html_test.text, "lxml")
    jobs = soup.find_all("span", {'data-text': 'true'})

    for j in jobs:
        for key, value in cons.CAT_LIST.items():
            for val in value:
                if re.search(f"\b{val.lower()}\b", j.text.lower()):
                    return cons.CAT_ID[key]
    return cons.CAT_ID["unknown"]
