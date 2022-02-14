import uvicorn
from fastapi import FastAPI, Response, Depends, status

from sqlalchemy.orm import Session

from WebService.repo import newsCategoriesRepo, timerRepo, userRepo
from WebService.schemas.schema import UserReg
from DataBaseService.models import models
from DataBaseService.db_setup import engine, get_db

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(response: Response, reg_form: UserReg, db: Session = Depends(get_db)):
    cat_list = newsCategoriesRepo.is_valid_categories(reg_form.categories, db)
    if not cat_list:
        print("Mistake in category")
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    if userRepo.does_exist(reg_form.email, db):
        print("email exist")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None
    timer_list = timerRepo.get_times(reg_form)
    if not timer_list:
        print("wrong times")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None

    new_user = userRepo.create_user(reg_form, db)
    newsCategoriesRepo.insert_by_user_id(new_user.id, cat_list, db)
    timerRepo.insert_times(new_user.id, timer_list, db)
    return new_user


if __name__ == "__main__":
    uvicorn.run(app)
