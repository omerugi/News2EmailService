from sqlalchemy.orm import Session

from DataBaseService.models import models
from WebService.schemas.schema import UserReg
from datetime import date


def create_user(reg_form: UserReg, db: Session):
    new_user = models.User(email=reg_form.email, subscription_type=reg_form.subscription_type.value,
                           sign_up_time=date.today())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def does_exist(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def check_sub_type(reg_form: UserReg, db: Session):
    sub = reg_form.subscription_type
