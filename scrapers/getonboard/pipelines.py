from db.python_mongo_tools import MongoInterfaces
from db.notify_model import NotifyModel
from datetime import datetime

from scrapers.getonboard import GetOnBoardScraper, GetOnBoardNotifyTransformer
from bots.telegram_notifier import NotifierBot
import os

Logger = "..... Cleaning the job {id} => {title}"


def basic_pipeline(parallel, not_scraper, not_clean):
    def f():

        date = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        print(f'....... {date} .......')

        admin_chat = os.getenv('CHAT')
        notifier = NotifierBot()
        notifier.push(
            admin_chat, f"The GetOnBoard Scraper has started for {date}")
        if not not_scraper:
            scraper = GetOnBoardScraper()
            scraper.save_all(
                filter_condition=lambda job: (
                    job["pinned"] or
                    type(job['published_at']) != datetime or
                    job['published_at'] >= date
                )
            )

        notifier.push(
            admin_chat, f"The GetOnBoard Scraper has started to clean the data")
        if not not_clean:
            print('....... Cleaning all jobs in GetOnBoard 🧐')
            db = MongoInterfaces('GetOnBoard')
            notify_db = NotifyModel()
            count = 0
            for job in db.all(created_at={'$gt': date}):
                tjob = GetOnBoardNotifyTransformer(job)
                notify_db.save(tjob)
                print(Logger.format(id=job['id'], title=job['title']))
                count += 0
            notifier.push(
                admin_chat, f"{count} jobs have been scraped and cleaned from GetOnBoard")

    return f
