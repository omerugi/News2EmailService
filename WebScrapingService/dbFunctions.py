from sqlalchemy import desc
from sqlalchemy.orm import Session

from DataBaseService.models.models import NewsArticles
from DataBaseService.db_setup import get_db


def does_headline_exist(head_line):
    return does_exist_by_feature(NewsArticles.head_line, head_line) is not None


def does_exist_by_feature(feature, search_term):
    db = Session(next(get_db()).bind)
    ans = db.query(NewsArticles).filter(feature == search_term).first()
    db.close()
    return ans


def insert_news(new_article: NewsArticles):
    db = Session(next(get_db()).bind)
    db.add(new_article)
    db.commit()
    db.close()


def last_update_by_page(page_code: str):
    db = Session(next(get_db()).bind)
    ans = db.query(NewsArticles.date_time).filter(NewsArticles.page_code == page_code).order_by(
        desc(NewsArticles.date_time)).first()
    db.close()
    return ans

