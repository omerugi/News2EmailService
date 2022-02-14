from typing import List
from sqlalchemy.orm import Session

from DataBaseService.models.models import NewsCategory, UserCat


def is_valid_categories(cat_list: List, db: Session):
    cat_code = []
    q = db.query(NewsCategory).all()
    for i in cat_list:
        temp = db.query(NewsCategory).filter(NewsCategory.category == i).first()
        if not temp:
            return None
        cat_code.append(temp.id)
    return cat_code


def insert_by_user_id(id, cat_list: List, db: Session):
    for i in cat_list:
        new_usercat = UserCat(user_id=id, cat_id=i)
        db.add(new_usercat)
        db.commit()
        db.refresh(new_usercat)


def delete_by_user_id(user_id, db: Session):
    return db.query(UserCat).filter(UserCat.user_id == user_id).delete(synchronize_session=False)
