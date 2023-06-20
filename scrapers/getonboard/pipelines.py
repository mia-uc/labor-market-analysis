from db.python_mongo_tools import MongoInterfaces
from db.notify_model import NotifyModel
from datetime import datetime

from scrapers.getonboard import GetOnBoardScraper, GetOnBoardNotifyTransformer
from bots.telegram_notifier import NotifierBot
import os

Logger = "..... Cleaning the job {id} => {title}"


def basic_pipeline(parallel, not_scraper, not_clean, first_time=True):
    def f():
        nonlocal first_time

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
            try:
                scraper.save_all(
                    filter_condition=lambda job: (
                        first_time or
                        job["pinned"] or
                        type(job['published_at']) != datetime or
                        job['published_at'] >= date
                    )
                )
            except KeyboardInterrupt:
                pass

            except Exception as e:
                notifier.error(admin_chat, f'GetOnBoard Scraper')
                raise e

        first_time = False

        if not not_clean:
            notifier.push(
                admin_chat,
                f"The GetOnBoard Scraper has started to clean the data"
            )

            print('....... Cleaning all jobs in GetOnBoard 🧐')
            db = MongoInterfaces('GetOnBoard')
            notify_db = NotifyModel()
            count = 0
            try:
                for job in db.all(cleaned_at={'$exists': False}):
                    print(Logger.format(id=job['id'], title=job['title']))
                    # Clean Job
                    tjob = GetOnBoardNotifyTransformer(job)
                    # Save cleaned job
                    notify_db.save(tjob)
                    # Update dirty job
                    db.update(
                        {'cleaned_at': date},
                        url=job['url'],
                        id=job['id']
                    )

                    count += 1
            except Exception as e:
                notifier.error(admin_chat, f'GetOnBoard ETL')
                raise e

            print(
                f"....... {count} jobs have been scraped and cleaned from GetOnBoard"
            )

            notifier.push(
                admin_chat, f"{count} jobs have been scraped and cleaned from GetOnBoard"
            )

    return f
