from fastapi import APIRouter, Response, Depends, status
from sqlalchemy.orm import Session
from DataBaseService.db_setup import get_db
from WebService.repo import newsCategoriesRepo, userRepo

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.post("/init_cat", status_code=status.HTTP_201_CREATED)
def init_categories(response: Response, db: Session = Depends(get_db)):
    newsCategoriesRepo.init_categories(db)


@router.get("/users", status_code=status.HTTP_201_CREATED)
def get_all_users(response: Response, db: Session = Depends(get_db)):
    return userRepo.get_all_users(db)
