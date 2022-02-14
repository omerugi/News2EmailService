from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from DataBaseService.db_setup import Base


class UserCat(Base):
    __tablename__ = 'user_cat'
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    cat_id = Column(ForeignKey('news_categories.id'), primary_key=True)
    user = relationship("User", back_populates="categories")
    cat = relationship("NewsCategory", back_populates="user")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    subscription_type = Column(String(20), index=True, nullable=False)
    last_update = Column(DateTime, index=True, nullable=False)

    # at_what_time = relationship("Timer", back_populates="user")
    categories = relationship("UserCat", back_populates="user")
    asap = relationship("AsapSub", uselist=False, back_populates="user")
    daily = relationship("DailySub", back_populates="user")
    weekly = relationship("WeeklySub", back_populates="user")


class AsapSub(Base):
    __tablename__ = "asap_subscription"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="asap")


class DailySub(Base):
    __tablename__ = "daily_subscription"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hour = Column(String(2), index=True, nullable=False)
    minutes = Column(String(2), index=True, nullable=False)
    am_pm = Column(String(2), index=True, nullable=False)
    user = relationship("User", back_populates="daily")


class WeeklySub(Base):
    __tablename__ = "weekly_subscription"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    day = Column(String(20), index=True, nullable=False)
    hour = Column(String(2), index=True, nullable=False)
    minutes = Column(String(2), index=True, nullable=False)
    am_pm = Column(String(2), index=True, nullable=False)
    user = relationship("User", back_populates="weekly")


class NewsCategory(Base):
    __tablename__ = "news_categories"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    user = relationship("UserCat", back_populates="cat")
    news = relationship("NewsArticles", back_populates="cat")


#
# class Timer(Base):
#     __tablename__ = "times"
#     id = Column(Integer, primary_key=True, index=True)
#     subscription_type = Column(String(20), index=True, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     user = relationship("User", back_populates="at_what_time")
#
#     day = Column(String(20), index=True, nullable=False)
#     hour = Column(String(2), index=True, nullable=False)
#     minutes = Column(String(2), index=True, nullable=False)
#     am_pm = Column(String(2), index=True, nullable=False)


class NewsArticles(Base):
    __tablename__ = "news_articles"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(100), index=True, nullable=False)
    head_line = Column(String(50), index=True, nullable=False)
    time = Column(String(50), index=True, nullable=False)
    date = Column(String(50), index=True, nullable=False)
    cat_id = Column(Integer, ForeignKey('news_categories.id'))
    cat = relationship("NewsCategory", back_populates="news")
