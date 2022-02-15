from datetime import datetime

from DataBaseService.models.models import AsapSub
from sqlalchemy.orm import Session


def get_asap_sub():
    return AsapSub(last_update=datetime.now())


def delete_by_user_id_without_commit(user_id, db: Session):
    return db.query(AsapSub).filter(AsapSub.user_id == user_id).delete(synchronize_session=False)
