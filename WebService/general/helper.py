import re
from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session
import constants as cons
from WebService.repo import newsCategoriesRepo, userRepo
from WebService.schemas.schema import UserReg, Timer
from DataBaseService.models.models import User


def is_valid_time(timer: Timer):
    s = timer.time.replace(" ", "").split(":")
    return 0 <= int(s[0]) <= 23 and 0 <= int(s[0]) < 60


def is_valid_categories(cat_list: List[str]):
    cat_code = []
    for i in cat_list:
        if i.lower() not in cons.CAT_ID:
            return None
        cat_code.append(cons.CAT_ID[i.lower()])
    return cat_code


# TODO: replace this - change to Repo's
def insert_subscriptions_without_commit(new_user: User, subscription, db: Session):
    subscription.user = new_user
    db.add(subscription)


def delete_user_from_all_db(user: User, db: Session):
    user_id = user.id
    newsCategoriesRepo.delete_by_user_id(user_id, db)
    userRepo.delete_user_by_email_without_commit(user.email, db)
    db.commit()


def is_valid_email(email: str):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return re.fullmatch(regex, email)


def get_date_by_offset(day: str):
    offset = (datetime.today().day - cons.DAYS_ID[day.lower()]) % 7
    if offset == 0:
        return datetime.today() - timedelta(days=7)
    return datetime.today() - timedelta(days=offset)


def is_valid_subscription(reg_form: UserReg):
    try:
        user_sub = cons.SUBSCRIPTION_TYPES[reg_form.subscription_type.lower()]
    except:
        return False
    if user_sub == 0:
        return True
    elif user_sub == 1 or user_sub == 2:
        if is_valid_time(reg_form.at_what_time):
            if user_sub == 2:
                return reg_form.at_what_time.day in cons.DAYS_ID
        return True

    return False


def set_up_time(timer: Timer, date: datetime):
    s = timer.time.replace(" ", "").split(":")
    return date.replace(hour=int(s[0]), minute=int(s[1]), second=0)


def last_update_by_subscription(reg_form):
    try:
        user_sub = cons.SUBSCRIPTION_TYPES[reg_form.subscription_type.lower()]
    except:
        return None
    if user_sub == 0:
        return user_sub, datetime.now()

    if not is_valid_time(reg_form.at_what_time):
        return None

    if user_sub == 1:
        return user_sub, set_up_time(reg_form.at_what_time, datetime.today() - timedelta(days=1))
    if user_sub == 2:
        return user_sub, set_up_time(reg_form.at_what_time, get_date_by_offset(reg_form.at_what_time.day))
    return None
