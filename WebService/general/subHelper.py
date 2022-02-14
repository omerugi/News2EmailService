from typing import List

from sqlalchemy.orm import Session

from WebService.repo import asapRepo, dailyRepo, weeklyRepo
from WebService.schemas.schema import UserReg, SubType, Timer


def is_valid_hour(hour):
    return 0 <= int(hour) <= 11


def is_valid_minutes(minutes):
    return 0 <= int(minutes) <= 59


def get_time_info_by_subtype(timer: Timer, sub_type: SubType):
    hour, minute, am_pm = timer.hour, timer.minutes, timer.am_pm
    if sub_type == SubType.Daily:
        return None, hour, minute, am_pm
    elif sub_type == SubType.Weekly:
        return timer.day, hour, minute, am_pm


def get_times(reg_form: UserReg):
    subtype = reg_form.subscription_type

    if subtype == SubType.ASAP:
        return [asapRepo.get_asap_sub()]
    elif subtype == SubType.Daily:
        try:
            timer_lst = []
            for t in reg_form.at_what_time:
                _, hour, minute, am_pm = get_time_info_by_subtype(t, subtype)
                if is_valid_hour(hour) and is_valid_minutes(minute):
                    timer_lst.append(dailyRepo.get_daily_sub(hour, minute, am_pm))
            return timer_lst
        except:
            return None
    elif subtype == SubType.Weekly:
        try:
            timer_lst = []

            # TODO: add is valid day
            for t in reg_form.at_what_time:
                day, hour, minute, am_pm = get_time_info_by_subtype(t, subtype)
                if is_valid_hour(hour) and is_valid_minutes(minute):
                    timer_lst.append(weeklyRepo.get_weekly_sub(day, hour, minute, am_pm))
            return timer_lst
        except:
            return None
    return None


def insert_times(user_id, timer_lst: List, db: Session):
    for t in timer_lst:
        t.user_id = user_id
        db.add(t)
        db.commit()


def delete_user_sub(user_id,user_sub, db):
    if user_sub == SubType.ASAP.value:
        return asapRepo.delete_by_user_id(user_id, db)
    elif user_sub == SubType.Daily.value:
        return dailyRepo.delete_by_user_id(user_id, db)
    elif user_sub == SubType.Weekly.value:
        return weeklyRepo.delete_by_user_id(user_id, db)
    return None