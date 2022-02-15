from DataBaseService.models.models import WeeklySub
from sqlalchemy.orm import Session

from WebService.schemas.schema import Timer


def get_weekly_sub(timer : Timer):
    try:
        return WeeklySub(time=timer.time, day = timer.day)
    except:
        return None


def delete_by_user_id_without_commit(user_id, db: Session):
    return db.query(WeeklySub).filter(WeeklySub.user_id == user_id).delete(synchronize_session=False)
