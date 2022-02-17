from sqlalchemy import desc
from sqlalchemy.orm import Session

from DataBaseService.models.models import NewsArticles
from DataBaseService.db_setup import get_db


def does_headline_exist(db: Session, head_line):
    return does_exist_by_feature(db, NewsArticles.head_line, head_line) is not None


def does_exist_by_feature(db: Session, feature, search_term):
    ans = db.query(NewsArticles).filter(feature == search_term).first()
    return ans


def insert_news(db: Session, new_article: NewsArticles):
    db.add(new_article)


def last_update_by_page(db: Session, page_code: str):
    ans = db.query(NewsArticles.date_time).filter(NewsArticles.page_code == page_code).order_by(
        desc(NewsArticles.date_time)).first()
    return ans


def commit(db: Session):
    db.commit()
