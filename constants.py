YNET_MAIN_PAGE_URL = "https://www.ynetnews.com/category/3089"
DB_URL = "postgresql+psycopg2://postgres:13qeadzc@localhost:5432/News2Email"
DATE_TIME_FORMAT = "%d.%m.%y;%H:%M"
YNET_DATE_TIME_FORMAT = "%m.%d.%y;%H:%M"
CAT_LIST = {
    "Sports": ["football", "basketball", "ski", "sport", "olympics", "athletics", "tournament"],
    "Politics": ["president", "prime minister", "law", "U.N", "NATO", "government",
                 "democrats", "republicans", "minister", "vote", "politician", "political party"],
    "Finance": ["president", "prime minister", "law", "U.N", "NATO", "government",
                "democrats", "republicans", "minister", "vote", "politician", "political party"],
    "Whether": ["rain", "snow", "sunny", "earthquake", "clouds", "storm", "flood"]
}
CAT_ID = {
    "Unknown": 0,
    "Sports": 1,
    "Politics": 2,
    "Finance": 3,
    "Whether": 4
}
