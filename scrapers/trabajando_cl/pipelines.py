from db.python_mongo_tools import MongoInterfaces
from db.notify_model import NotifyModel
from datetime import datetime

from scrapers.trabajando_cl import WorkingCLScraper, WorkingCLNotifyTransformer
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

        if not not_scraper:
            notifier.push(
                admin_chat,
                f"The WorkingCL Scraper has started for {date}"
            )

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
            except Exception as e:
                notifier.error(admin_chat, f'WorkingCL Scraper')
                raise e

        first_time = False
        if not not_clean:
            # notifier.push(
            #     admin_chat,
            #     f"The WorkingCL Scraper has started to clean the data"
            # )

            print('....... Cleaning all jobs in WorkingCL 🧐')
            db = MongoInterfaces('Trabajando.cl')
            notify_db = NotifyModel()

            count = 0
            try:
                for job in db.all(cleaned_at={'$exists': False}):

                    # Clean Job
                    tjob = WorkingCLNotifyTransformer(job)

                    print(Logger.format(id=tjob.idOferta, title=tjob.name))

                    # Save cleaned job
                    notify_db.save(tjob)
                    # Update dirty job
                    db.update({'cleaned_at': date}, idOferta=job['idOferta'])

                    count += 1
            except Exception as e:
                notifier.error(admin_chat, f'WorkingCL ETL')
                raise e

            print(
                f"....... {count} jobs have been scraped and cleaned from WorkingCL"
            )
            notifier.push(
                admin_chat, f"{count} jobs have been scraped and cleaned from WorkingCL"
            )

    return f

# TODO: Levantar chile trabajos
# TODO: Revisar Laborum
