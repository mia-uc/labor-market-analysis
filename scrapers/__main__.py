from typer import Option, Typer
from db.python_mongo_tools import MongoInterfaces
from db.notify_model import NotifyModel
from datetime import datetime

from scrapers.getonboard import GetOnBoardScraper, GetOnBoardNotifyTransformer
from scrapers.laborum import LaborumScraper
from dotenv import load_dotenv
from bots.telegram_notifier import NotifierBot
import os


load_dotenv()
app = Typer()

Logger = "..... Cleaning the job {id} => {title}"

date = datetime.utcnow().replace(
    hour=0, minute=0, second=0, microsecond=0
)
print(f'....... {date} .......')


@app.command()
def getonbrd(
    parallel: bool = Option(False, "--parallel"),
    not_scraper: bool = Option(False, "--not_scraper"),
    not_clean: bool = Option(False, "--not_clean"),
):

    admin_chat = os.getenv('CHAT')
    notifier = NotifierBot()
    notifier.push(admin_chat, f"The GetOnBoard Scraper has started for {date}")
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


@app.command()
def laborum(parallel: bool = Option(False, "--parallel")):
    date = datetime.utcnow().date()

    scraper = LaborumScraper()
    scraper.save_all(
        filter_condition=lambda job: (
            type(job['published_at']) != datetime or
            job['published_at'].date() >= date
        )
    )

    db = MongoInterfaces('GetOnBoard')
    notify_db = MongoInterfaces('NotifyDB')
    for job in db.all(created_at=date):
        tjob = GetOnBoardNotifyTransformer(job)

        if notify_db.exists(id=tjob.id, origin='GetOnBoard'):
            notify_db.update(tjob.to_dict(), id=tjob.id, origin='GetOnBoard')
        else:
            notify_db.insert(tjob.to_dict())

        print(Logger.format(id=job['id'], title=job['title']))


if __name__ == '__main__':
    app()
