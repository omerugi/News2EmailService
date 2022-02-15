from DataBaseService.models.models import DailySub
from sqlalchemy.orm import Session

from WebService.schemas.schema import Timer


def get_daily_sub(timer : Timer):
    try:
        return DailySub(time=timer.time)
    except:
        return None


def delete_by_user_id_without_commit(user_id, db: Session):
    return db.query(DailySub).filter(DailySub.user_id == user_id).delete(synchronize_session=False)
