from fastapi import APIRouter, Response, Depends, status
from sqlalchemy.orm import Session
from WebService.repo import newsCategoriesRepo, userRepo
from WebService.schemas.schema import UserReg
from WebService.general import subHelper, userHelper
from DataBaseService.db_setup import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(response: Response, reg_form: UserReg, db: Session = Depends(get_db)):
    cat_list = newsCategoriesRepo.is_valid_categories(reg_form.categories, db)
    if not cat_list:
        print("Mistake in category")
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    if not userHelper.is_valid_email(reg_form.email):
        print("not a valid email")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None

    if userRepo.get_user_by_email(reg_form.email, db):
        print("email exist")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None

    subscription = subHelper.get_subscriptions(reg_form)

    if not subscription:
        print("wrong times")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None

    new_user = userRepo.create_and_insert_new_user_without_commit(reg_form, db)
    newsCategoriesRepo.insert_user_categories_by_id_without_commit(new_user.id, cat_list, db)
    subHelper.insert_subscriptions_without_commit(new_user, subscription, db)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/delete/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(email, response: Response, db: Session = Depends(get_db)):
    user = userRepo.get_user_by_email(email, db)
    if not user:
        print("email does not exist")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None
    userHelper.delete_user_from_all_db(user, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



