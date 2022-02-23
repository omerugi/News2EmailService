# News 2 Email Service

In this project, I've implemented an email subscription service, users signup with their email - selecting subscription type and news categories they are interested in, and get emails with relevant articles right to their in box!

## Subscriptions 
The users can select between:
1. Weekly sub - at what day and what time he wises to get updates.
2. Daily sub - at what time everyday he wises to get updates.
3. ASAP sub - as soon as a new relevent artical is up get an update.


## Database
I've used the Postgres database to store the information.
The tables:
1. users  - containing user info.
2. news_categories - all the categories for articles.
3. user_cat - many-to-many between users and news_categories, all the categories that each user picked.
4. news_articles - all the news it collects when scraping.

The implementation in Python done using SQLalchemy.

## Web Service
An API web server that was implemented using FastAPI.

## Web Scraping Service
Used Beutifulsuop to collect articles from websites and store then in the DB.

## Email Service
Sends emails using SMTP.
