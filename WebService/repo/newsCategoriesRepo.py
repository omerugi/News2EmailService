from typing import List
from sqlalchemy.orm import Session

from DataBaseService.models.models import NewsCategory, UserCat
import constants as cons


def is_valid_categories(cat_list: List, db: Session):
    cat_code = []
    for i in cat_list:
        temp = db.query(NewsCategory).filter(NewsCategory.category == i).first()
        if not temp:
            return None
        cat_code.append(temp.id)
    return cat_code


def insert_user_categories_by_id_without_commit(user_id, cat_list: List, db: Session):
    for i in cat_list:
        new_user_cat = UserCat(user_id=user_id, cat_id=i)
        db.add(new_user_cat)


def delete_by_user_id(user_id, db: Session):
    return db.query(UserCat).filter(UserCat.user_id == user_id).delete(synchronize_session=False)


def get_all_cat(db: Session):
    return db.query(NewsCategory).all()


def init_categories(db: Session):
    for key, value in cons.CAT_ID.items():
        if not db.query(NewsCategory).filter(NewsCategory.category == key).first():
            db.add(NewsCategory(id=value, category=key))

    db.commit()
    return None
