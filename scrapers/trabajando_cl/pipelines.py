from db.python_mongo_tools import MongoInterfaces
from db.notify_model import NotifyModel
from datetime import datetime

from scrapers.trabajando_cl import WorkingCLScraper, WorkingCLNotifyTransformer
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
            admin_chat, f"The WorkingCL Scraper has started for {date}")
        if not not_scraper:
            scraper = WorkingCLScraper()
            try:
                scraper.save_all(
                    filter_condition=lambda job: (
                        first_time or
                        type(job['published_at']) != datetime or
                        job['published_at'] >= date
                    )
                )
            except KeyboardInterrupt:
                pass

        first_time = False
        notifier.push(
            admin_chat, f"The WorkingCL Scraper has started to clean the data")
        if not not_clean:
            print('....... Cleaning all jobs in WorkingCL 🧐')
            db = MongoInterfaces('Trabajando.cl')
            notify_db = NotifyModel()
            count = 0
            for job in db.all(created_at={'$gt': date}):
                tjob = WorkingCLNotifyTransformer(job)
                notify_db.save(tjob)
                print(Logger.format(id=job['id'], title=job['title']))
                count += 1
            notifier.push(
                admin_chat, f"{count} jobs have been scraped and cleaned from WorkingCL")

    return f
