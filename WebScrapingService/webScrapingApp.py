from WebScrapingService import ynetPage
from DataBaseService.models import models
from DataBaseService.db_setup import engine
import schedule
import time
models.Base.metadata.create_all(engine)

def run():
    schedule.every(5).minutes.do(ynetPage.update_ynet_news)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    pass




