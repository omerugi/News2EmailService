from typing import List

from sqlalchemy.orm import Session

from WebService.repo import asapRepo, dailyRepo, weeklyRepo
from WebService.schemas.schema import UserReg, SubType, Timer
from DataBaseService.models.models import User


def is_valid_hour(hour):
    return 0 <= int(hour) <= 11


def is_valid_minutes(minutes):
    return 0 <= int(minutes) <= 59


# def get_time_info_by_subtype(timer: Timer, sub_type: SubType):
#     hour, minute, am_pm = timer.hour, timer.minutes, timer.am_pm
#     if sub_type == SubType.Daily:
#         return None, hour, minute, am_pm
#     elif sub_type == SubType.Weekly:
#         return timer.day, hour, minute, am_pm

def is_valid_time(timer: Timer):
    s = timer.time.replace(" ", "").split(":")
    return 0 <= int(s[0]) <= 23 and 0 <= int(s[0]) < 60


def get_subscriptions(reg_form: UserReg):
    subtype = reg_form.subscription_type

    if subtype == SubType.ASAP:
        return asapRepo.get_asap_sub()
    elif subtype == SubType.Daily:
        timer = reg_form.at_what_time
        if is_valid_time(timer):
            return dailyRepo.get_daily_sub(timer)

    elif subtype == SubType.Weekly:
        timer = reg_form.at_what_time
        # TODO: Check valid date
        if is_valid_time(timer):
            return weeklyRepo.get_weekly_sub(timer)
    return None


# TODO: replace this - change to Repo's
def insert_subscriptions_without_commit(new_user: User, subscription, db: Session):
    subscription.user = new_user
    db.add(subscription)


def delete_user_subscriptions(user_id, user_sub, db):
    if user_sub == SubType.ASAP.value:
        return asapRepo.delete_by_user_id_without_commit(user_id, db)
    elif user_sub == SubType.Daily.value:
        return dailyRepo.delete_by_user_id_without_commit(user_id, db)
    elif user_sub == SubType.Weekly.value:
        return weeklyRepo.delete_by_user_id_without_commit(user_id, db)
    return None
