import uvicorn
from fastapi import FastAPI
from DataBaseService.models import models
from DataBaseService.db_setup import engine
from WebService.routers.user_api import router as user_router
from WebService.routers.admin_api import router as admin_router


app = FastAPI()
models.Base.metadata.create_all(engine)
app.include_router(user_router)
app.include_router(admin_router)


def run():
    uvicorn.run(app)

if __name__ == "__main__":
    pass
