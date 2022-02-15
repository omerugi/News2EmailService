from EmailService.repo import userEmailRepo


def send_email_to_users():
    all_asap_subs = userEmailRepo.get_all_asap_subs()
    for user in all_asap_subs:
        print(user)
        ans = userEmailRepo.get_news_by_cat_id_and_last_update(user)
    pass
