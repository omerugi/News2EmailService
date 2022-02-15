from datetime import datetime

from bs4 import BeautifulSoup
import requests

import constants as cons
from DataBaseService.models.models import NewsArticles
from DataBaseService.db_setup import get_db
from tqdm import tqdm

def get_news_category(url: str):
    html_test = requests.get(url)
    soup = BeautifulSoup(html_test.text, "lxml")
    jobs = soup.find_all("span", {'data-text': 'true'})

    for j in jobs:
        for key, value in cons.CAT_LIST.items():
            for val in value:
                if val.lower() in j.text.lower():
                    return cons.CAT_ID[key]
    return cons.CAT_ID["Unknown"]


def is_headline_exist(head_line):
    db = next(get_db())
    if db.query(NewsArticles).filter(NewsArticles.head_line == head_line).first():
        db.close()
        return True
    db.close()
    return False


def get_formated_datetime_from_news(details):
    split_date = details.split(",")
    time = split_date[0]
    date = split_date[1]
    clear_datetime = date + ";" + time
    return datetime.strptime(clear_datetime, cons.YNET_DATE_TIME_FORMAT).strftime(cons.DATE_TIME_FORMAT)


def update_ynet_news():
    html_test = requests.get(cons.YNET_MAIN_PAGE_URL)
    soup = BeautifulSoup(html_test.text, "lxml")
    jobs = soup.find_all("div", class_="slotView")
    for j in tqdm(jobs):
        article = BeautifulSoup(str(j), "lxml")
        url = article.find("a").get("href")
        head_line = article.find("a").text
        if is_headline_exist(head_line):
            break
        date_time = get_formated_datetime_from_news(article.find("span", class_="dateView").text.replace(" ", ""))
        category = get_news_category(url)
        new_article = NewsArticles(url=url, head_line=head_line, date_time=date_time, cat_id=category)
        insert_news(new_article)


def insert_news(new_artivle: NewsArticles):
    db = next(get_db())
    db.add(new_artivle)
    db.commit()
    db.close()
