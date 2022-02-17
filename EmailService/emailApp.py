from DataBaseService.db_setup import engine
from DataBaseService.models import models
from EmailService import emailSender
import constants as cons
import schedule
import time

models.Base.metadata.create_all(engine)


def send_asap():
    emailSender.send_email_to_asap_sub()


def send_weekly_daily():
    users = emailSender.get_todays_sub()
    for user in users:
        emailSender.send_schedualed_email_user(user)


def run():
    schedule.every().day.at("00:00").do(send_weekly_daily)
    schedule.every(5).minutes.do(send_asap)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    pass
