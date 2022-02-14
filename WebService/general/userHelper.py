from DataBaseService.models.models import User
from sqlalchemy.orm import Session
from WebService.general import subHelper
from WebService.repo import userRepo, newsCategoriesRepo


def delete_user_from_all_db(user: User, db: Session):
    user_id = user.id
    user_sub = user.subscription_type
    subHelper.delete_user_sub(user_id, user_sub, db)
    newsCategoriesRepo.delete_by_user_id(user_id, db)
    userRepo.delete_user_by_email_without_commit(user.email, db)
    db.commit()