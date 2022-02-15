from sqlalchemy import tuple_
from sqlalchemy.orm import Session
from datetime import datetime

from DataBaseService.db_setup import get_db
from DataBaseService.models.models import AsapSub, User, UserCat, NewsArticles


def get_all_asap_subs():
    db = Session(next(get_db()).bind)
    ans = db.query(AsapSub, User.email).join(User).filter(AsapSub.user_id == User.id).all()
    db.close()
    return ans


def get_user_cat_by_id(user_id):
    db = Session(next(get_db()).bind)
    user_cat = db.query(UserCat.cat_id).filter(UserCat.user_id == user_id).all()
    db.close()
    return user_cat


def get_news_by_cat_id_and_last_update(user):
    db = Session(next(get_db()).bind)
    user_id = user.id
    news = db.query(NewsArticles).filter(tuple_(NewsArticles.cat_id, ).in_(
        get_user_cat_by_id(user.id)) | NewsArticles.date_time > user.last_update).all()
    return news
