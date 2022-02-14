from DataBaseService.models.models import WeeklySub
from sqlalchemy.orm import Session


def get_weekly_sub(day, hour, minute, am_pm):
    try:
        return WeeklySub(day=day, hour=hour, minutes=minute, am_pm=am_pm.value)
    except:
        return None


def delete_by_user_id(user_id, db: Session):
    return db.query(WeeklySub).filter(WeeklySub.user_id == user_id).delete(synchronize_session=False)
