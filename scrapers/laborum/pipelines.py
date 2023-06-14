from db.python_mongo_tools import MongoInterfaces
from db.notify_model import NotifyModel
from datetime import datetime

from scrapers.laborum import LaborumScraper, LaborumNotifyTransformer
from bots.telegram_notifier import NotifierBot
import os

Logger = "..... Cleaning the job {id} => {title}"


def basic_pipeline(parallel, not_scraper, not_clean):
    first_time = True

    def f():
        nonlocal first_time

        date = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        print(f'....... {date} .......')

        admin_chat = os.getenv('CHAT')
        notifier = NotifierBot()
        notifier.push(
            admin_chat, f"The Laborum Scraper has started for {date}")
        if not not_scraper:
            scraper = LaborumScraper()
            scraper.save_all(
                filter_condition=lambda job: (
                    first_time or
                    type(job['fechaPublicacion']) != datetime or
                    job['fechaPublicacion'] >= date
                )
            )

        first_time = False
        notifier.push(
            admin_chat, f"The Laborum Scraper has started to clean the data")
        if not not_clean:
            print('....... Cleaning all jobs in Laborum 🧐')
            db = MongoInterfaces('Laborum')
            notify_db = NotifyModel()
            count = 0
            for job in db.all(created_at={'$gt': date}):
                tjob = LaborumNotifyTransformer(job)
                notify_db.save(tjob)
                print(Logger.format(id=job['id'], title=job['titulo']))
                count += 1
            notifier.push(
                admin_chat, f"{count} jobs have been scraped and cleaned from Laborum")

    return f
