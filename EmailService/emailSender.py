from datetime import datetime, timedelta

from tqdm import tqdm
from typing import List
from DataBaseService.models.models import NewsArticles, User
from EmailService import dbFunctions
import constants as cons
import smtplib
from email.message import EmailMessage


def send_email_to_users_by_sub_and_lastupdate(sub: int, time: datetime = datetime.now()):
    all_user_by_subs = dbFunctions.get_all_users_by_sub_and_lastupdate(sub, time)
    users_to_update = []
    for user in tqdm(all_user_by_subs):
        user_articles = dbFunctions.get_news_by_cat_id_and_lastupdate(user)
        if user_articles:
            users_to_update.append((user.id,))
            send_email_to_user(
                create_EmailMessage(user.email,
                                    format_email_for_user(user_articles)))
    if users_to_update:
        dbFunctions.update_users_lastupdate(users_to_update, get_timedelta_by_sub(sub))


def update_users_lastupdate(users_to_update):
    if users_to_update[cons.DAILY]:
        dbFunctions.update_users_lastupdate(users_to_update[cons.DAILY], get_timedelta_by_sub(cons.DAILY))
    if users_to_update[cons.WEEKLY]:
        dbFunctions.update_users_lastupdate(users_to_update[cons.WEEKLY], get_timedelta_by_sub(cons.WEEKLY))


def send_email_to_weekly_and_daily_by_lastupdate():
    all_user_by_subs = dbFunctions.get_all_users_by_two_sub_and_lastupdate(cons.WEEKLY, cons.DAILY)
    users_to_update = {cons.DAILY: [], cons.WEEKLY: []}
    for user in tqdm(all_user_by_subs):
        user_articles = dbFunctions.get_news_by_cat_id_and_lastupdate(user)
        if user_articles:
            users_to_update[user.subscription_type].append((user.id,))
            send_email_to_user(
                create_EmailMessage(user.email,
                                    format_email_for_user(user_articles)))
    update_users_lastupdate(users_to_update)


def get_timedelta_by_sub(sub: int):
    if sub == 0:
        return timedelta(days=0, minutes=5)
    if sub == 1:
        return timedelta(days=1)
    if sub == 2:
        return timedelta(days=7)


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
