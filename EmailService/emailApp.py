from DataBaseService.db_setup import engine
from DataBaseService.models import models
from EmailService import emailSender
import constants as cons

models.Base.metadata.create_all(engine)

if __name__ == '__main__':
    # emailSender.send_email_to_users_by_sub_and_lastupdate(cons.ASAP)
    emailSender.send_email_to_weekly_and_daily_by_lastupdate()
    # TODO: make a scheduler - asap: every 10 min, daily+weekly: get times every 24 hour.
