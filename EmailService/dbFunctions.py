from datetime import timedelta, datetime
from typing import List

from sqlalchemy import tuple_, and_, or_
from sqlalchemy.orm import Session
from DataBaseService.db_setup import get_db
from DataBaseService.models.models import User, UserCat, NewsArticles


def get_all_users_by_sub_and_lastupdate(sub: int, time: datetime = datetime.now()):
    db = Session(next(get_db()).bind)
    ans = db.query(User).filter(and_(User.subscription_type == sub, User.last_update <= time)).all()
    db.close()
    return ans


def get_all_users_by_two_sub_and_lastupdate(sub1: int, sub2: int):
    db = Session(next(get_db()).bind)
    ans = db.query(User).filter(and_
        (or_(User.subscription_type == sub1, User.subscription_type == sub2) , or_(User.last_update <= datetime.now()))).all()
    db.close()
    return ans


def get_user_cat_by_id(user_id: str):
    db = Session(next(get_db()).bind)
    user_cat = db.query(UserCat.cat_id).filter(UserCat.user_id == user_id).all()
    db.close()
    return user_cat


def get_news_by_cat_id_and_lastupdate(user):
    db = Session(next(get_db()).bind)
    news = db.query(NewsArticles).filter(tuple_(NewsArticles.cat_id, ).in_(
        get_user_cat_by_id(user.id)) & (NewsArticles.date_time > user.last_update)).all()
    db.close()
    return news


def update_users_lastupdate(users: List, move_update: timedelta):
    db = Session(next(get_db()).bind)
    db.query(User).filter(tuple_(User.id, ).in_(users)).update(
        {User.last_update: User.last_update + move_update})
    db.commit()
    db.close()
    return None
