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
    subscription_type = Column(Integer, index=True, nullable=False)
    last_update = Column(DateTime, index=True, nullable=False)
    categories = relationship("UserCat", back_populates="user")


class NewsCategory(Base):
    __tablename__ = "news_categories"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    user = relationship("UserCat", back_populates="cat")
    news = relationship("NewsArticles", back_populates="cat")


class NewsArticles(Base):
    __tablename__ = "news_articles"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(100), index=True, nullable=False)
    head_line = Column(String(255), index=True, nullable=False)
    date_time = Column(DateTime, index=True, nullable=False)
    cat_id = Column(Integer, ForeignKey('news_categories.id'))
    page_code = Column(String(3), index=True, nullable=False)
    cat = relationship("NewsCategory", back_populates="news")


# class NewsPageUpdate(Base):
#     __tablename__ = "news_page_update"
#     id = Column(Integer, primary_key=True, index=True)
#     page_code = Column(String(3), index=True, nullable=False)
#     last_update = Column(DateTime, index=True, nullable=False)
