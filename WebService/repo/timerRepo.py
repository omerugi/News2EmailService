from typing import List

from DataBaseService.models import models
from WebService.schemas.schema import UserReg
from sqlalchemy.orm import Session
from WebService.schemas.schema import SubType


def is_valid_hour(hour):
    return 0 <= hour <= 11


def is_valid_minutes(minutes):
    return 0 <= minutes <= 59


def get_times(reg_form: UserReg):
    subtype = reg_form.subscription_type
    timer_list = reg_form.at_what_time
    timer = []
    if subtype == SubType.ASAP and is_valid_hour(timer_list[0].hour) and is_valid_minutes(timer_list[0].minutes):
        timer.append(
            models.Timer(day="ASAP", hour=timer_list[0].hour, minutes=timer_list[0].minutes, am_pm=timer_list[0].am_pm,
                         subscription_type="ASAP"))
    elif subtype == SubType.Daily:
        for t in timer_list:
            if is_valid_hour(t.hour) and is_valid_minutes(t.minutes):
                timer.append(
                    models.Timer(day="Everyday", hour=t.hour, minutes=t.minutes, am_pm=t.am_pm,
                                 subscription_type="Daily"))
    elif subtype == SubType.Weekly:
        for t in timer_list:
            timer.append(models.Timer(day=t.day, hour=timer_list[0].hour, minutes=timer_list[0].minutes, am_pm=t.am_pm,
                                      subscription_type="Weekly"))
    else:
        return None

    return timer


def insert_times(user_id, timer_lst: List[models.Timer], db: Session):
    for t in timer_lst:
        t.user_id = user_id
        db.add(t)
        db.commit()
        db.refresh(t)
