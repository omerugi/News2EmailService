import threading
from datetime import date, datetime
from datetime import timedelta

from EmailService import emailApp
from WebScrapingService import webScrapingApp
from WebService import mainAPI

if __name__ == '__main__':
    t1 = threading.Thread(target=emailApp.run)
    t2 = threading.Thread(target=webScrapingApp.run)
    t3 = threading.Thread(target=mainAPI.run)
    t1.start()
    t2.start()
    t3.start()
    pass
