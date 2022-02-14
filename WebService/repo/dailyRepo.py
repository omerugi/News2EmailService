from DataBaseService.models.models import DailySub
from WebService.schemas.schema import AmPm
from sqlalchemy.orm import Session

def get_daily_sub(hour, minute, am_pm: AmPm):
    try:
        return DailySub(hour=hour, minutes=minute, am_pm=am_pm.value)
    except:
        return None


def delete_by_user_id(user_id, db: Session):
    return db.query(DailySub).filter(DailySub.user_id == user_id).delete(synchronize_session=False)