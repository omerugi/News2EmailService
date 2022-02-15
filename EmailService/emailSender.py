from DataBaseService.db_setup import engine
from DataBaseService.models import models
from EmailService.emailBuilders import asapMailBuilder

models.Base.metadata.create_all(engine)



if __name__ == '__main__':
    asapMailBuilder.send_email_to_users()
