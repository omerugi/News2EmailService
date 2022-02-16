YNET_MAIN_PAGE_URL = "https://www.ynetnews.com/category/3089"
DB_URL = "postgresql+psycopg2://postgres:13qeadzc@localhost:5432/News2Email"

DATE_TIME_FORMAT = "%d.%m.%y;%H:%M"
YNET_DATE_TIME_FORMAT = "%m.%d.%y;%H:%M"

CAT_LIST = {
    "sports": ["football", "basketball", "ski", "sport", "olympics", "athletics", "tournament"],
    "politics": ["president", "prime minister", "law", "U.N", "NATO", "government",
                 "democrats", "republicans", "minister", "vote", "politician", "political party", "Bennett", "Hamas"],
    "finance": ["president", "prime minister", "law", "U.N", "NATO", "government",
                "democrats", "republicans", "minister", "vote", "politician", "political party"],
    "whether": ["rain", "snow", "sunny", "earthquake", "clouds", "storm", "flood"]
}
CAT_ID = {
    "unknown": 0,
    "sports": 1,
    "politics": 2,
    "finance": 3,
    "whether": 4
}
DAYS_ID = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

SUBSCRIPTION_TYPES = {
    "asap": 0,
    "daily": 1,
    "weekly": 2
}
ASAP = SUBSCRIPTION_TYPES["asap"]
WEEKLY = SUBSCRIPTION_TYPES["weekly"]
DAILY = SUBSCRIPTION_TYPES["daily"]

PAGE_TYPES = {
    "ynet": "YNT"
}
YNET_PAGE_CODE = PAGE_TYPES["ynet"]

EMAIL_ADDRESS = "sightbitproject@gmail.com"
EMAIL_PASSWORD = "13qeadzc"
