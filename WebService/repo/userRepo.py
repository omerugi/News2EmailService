from sqlalchemy.orm import Session

from DataBaseService.models.models import User
from WebService.schemas.schema import UserReg
from datetime import datetime


def create_and_insert_new_user_without_commit(reg_form: UserReg, db: Session):
    print(datetime.now())
    new_user = User(email=reg_form.email, subscription_type=reg_form.subscription_type.value)
    db.add(new_user)
    return new_user


def get_user_by_email(email, db: Session):
    return db.query(User).filter(User.email == email).first()


def delete_user_by_email_without_commit(email, db: Session):
    return db.query(User).filter(User.email == email).delete(synchronize_session=False)


def get_all_users(db):
    return db.query(User).all()
