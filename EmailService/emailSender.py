from datetime import datetime, timedelta
import time
from DataBaseService.db_setup import SessionLocal
from tqdm import tqdm
from typing import List
from DataBaseService.models.models import NewsArticles, User
from EmailService import dbFunctions
import constants as cons
import smtplib
from email.message import EmailMessage


def get_latest_news_update_time(db):
    last_article = dbFunctions.last_updated_article(db)
    if not last_article:
        return datetime.now()
    return last_article.date_time


def send_email_to_asap_sub():
    with SessionLocal() as db:
        last_article_update = get_latest_news_update_time(db)
        all_user_by_subs = dbFunctions.get_all_users_by_sub_and_lastupdate(db, cons.ASAP, last_article_update)
        users_to_update = []
        for user in tqdm(all_user_by_subs):
            user_articles = dbFunctions.get_news_by_cat_id_and_lastupdate(db, user)
            if user_articles:
                users_to_update.append((user.id, user.last_update))
                send_email_to_user(
                    create_EmailMessage(user.email,
                                        format_email_for_user(user_articles)))
        if users_to_update:
            dbFunctions.update_users_lastupdate_by_datetime(db, users_to_update,
                                                            get_updated_time(datetime.now(), cons.ASAP))
        dbFunctions.commit(db)


# def send_email_to_weekly_and_daily_sub():
#     with SessionLocal() as db:
#         last_article_update = get_latest_news_update_time(db)
#         all_user_by_subs = dbFunctions.get_all_users_by_two_sub_and_lastupdate(db, cons.WEEKLY, cons.DAILY,
#                                                                                last_article_update)
#         users_to_update = {cons.DAILY: [], cons.WEEKLY: []}
#         for user in tqdm(all_user_by_subs):
#             user_articles = dbFunctions.get_news_by_cat_id_and_lastupdate(db, user)
#             if user_articles:
#                 users_to_update[user.subscription_type].append((user.id, user.last_update))
#                 send_email_to_user(
#                     create_EmailMessage(user.email,
#                                         format_email_for_user(user_articles)))
#         update_users_lastupdate(db, users_to_update)
#         dbFunctions.commit(db)


# def update_users_lastupdate(db, users_to_update):
#     if users_to_update[cons.DAILY]:
#         for user_tuple in users_to_update[cons.DAILY]:
#             dbFunctions.update_user_lastupdate(db, user_tuple[0], get_updated_time(user_tuple[1], cons.DAILY))
#     if users_to_update[cons.WEEKLY]:
#         for user_tuple in users_to_update[cons.WEEKLY]:
#             dbFunctions.update_user_lastupdate(db, user_tuple[0], get_updated_time(user_tuple[1], cons.WEEKLY))


def get_updated_time(user_time, sub):
    if sub == 0:
        return datetime.now() + timedelta(days=0, minutes=5)
    if sub == 1:
        return datetime.now().replace(hour=user_time.hour, minute=user_time.hour) + timedelta(days=1)
    if sub == 2:
        return datetime.now().replace(hour=user_time.hour, minute=user_time.hour) + timedelta(days=7)


def format_email_for_user(articles: List[NewsArticles]):
    if not articles:
        return None
    subject = ""
    for article in articles:
        subject += f"{article.head_line} \n {article.url} \n"
    return subject


def create_EmailMessage(email: str, articles: str):
    if not articles:
        return None
    msg = EmailMessage()
    msg['Subject'] = "New2Email Update!"
    msg['From'] = cons.EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(articles)
    return msg


def send_email_to_user(msg: EmailMessage):
    if not msg:
        return None
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(cons.EMAIL_ADDRESS, cons.EMAIL_PASSWORD)
        smtp.send_message(msg)
    pass


def get_todays_sub():
    ans = ""
    with SessionLocal() as db:
        ans = dbFunctions.get_todays_users_by_sub(db, cons.DAILY, cons.WEEKLY)
    return ans


def send_schedualed_email_user(user: User):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(cons.EMAIL_ADDRESS, cons.EMAIL_PASSWORD)

        msg = EmailMessage()
        msg['Subject'] = "New2Email Update!"
        msg['From'] = cons.EMAIL_ADDRESS
        msg['To'] = user.email
        with SessionLocal as db:
            time.sleep(user.last_update.timestamp() - time.time())
            user_articles = dbFunctions.get_news_by_cat_id_and_lastupdate(db, user)
            if user_articles:
                msg.set_content(format_email_for_user(user_articles))
                smtp.send_message(msg)
                dbFunctions.update_user_lastupdate(db, user.id,
                                                   get_updated_time(user.last_update, user.subscription_type))
            else:
                return
