
from WebScrapingService.repo import newsArticalRepo
from DataBaseService.models import models
from DataBaseService.db_setup import engine

models.Base.metadata.create_all(engine)

if __name__ == '__main__':
    newsArticalRepo.update_ynet_news()




