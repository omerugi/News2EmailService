from datetime import timedelta, datetime
from typing import List

from sqlalchemy import tuple_, and_, or_, desc, asc
from sqlalchemy.orm import Session
from DataBaseService.models.models import User, UserCat, NewsArticles


def get_all_users_by_sub_and_lastupdate(db: Session, sub: int, last_article):
    ans = db.query(User).filter(
        and_(
            User.subscription_type == sub,
            User.last_update <= datetime.now(),
            User.last_update <= last_article
        )
    ).all()
    return ans


# def get_all_users_by_two_sub_and_lastupdate(db: Session, sub1: int, sub2: int, last_article):
#     ans = db.query(User).filter(
#         and_(
#             or_(User.subscription_type == sub1, User.subscription_type == sub2),
#             User.last_update <= datetime.now(),
#             User.last_update <= last_article
#         )
#     ).all()
#     return ans


def get_user_cat_by_id(db: Session, user_id: str):
    user_cat = db.query(UserCat.cat_id).filter(UserCat.user_id == user_id).all()
    return user_cat


def get_news_by_cat_id_and_lastupdate(db: Session, user):
    news = db.query(NewsArticles).filter(and_(
        tuple_(NewsArticles.cat_id, ).in_(get_user_cat_by_id(db, user.id)),
        NewsArticles.date_time > user.last_update
                                            )
                                        ).all()
    return news


def update_user_lastupdate(db: Session, user_id: int, update_date: datetime):
    db.query(User).filter(User.id == user_id).update(
        {
            User.last_update: update_date
        }
    )


def update_users_lastupdate_by_datetime(db: Session, users: List, date_update: datetime):
    db.query(User).filter(tuple_(User.id, ).in_(users)).update(
        {User.last_update: date_update})


def last_updated_article(db: Session):
    ans = db.query(NewsArticles.date_time).order_by(desc(NewsArticles.date_time)).first()
    return ans


def commit(db: Session):
    db.commit()


def get_todays_users_by_sub(db: Session, sub1, sub2):
    tommorow = datetime.now().replace(hour=00, minute=00) + timedelta(days=1)
    yersterday = datetime.now().replace(hour=23, minute=59, second=59) - timedelta(days=1)
    return db.query(User).filter(
        and_(
            or_(User.subscription_type == sub1, User.subscription_type == sub2),
            and_(yersterday < User.last_update, User.last_update < tommorow)
        )
    ).order_by(asc(User.last_update)).all()



