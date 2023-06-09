from typer import Option, Typer
from datetime import datetime
from scrapers.getonboard.pipelines import basic_pipeline
from dotenv import load_dotenv

import schedule
import time


load_dotenv()
app = Typer()


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
    func = basic_pipeline(
        date, parallel, not_scraper, not_clean
    )
    schedule.every(24).hours.do(func)

    func()
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.command()
def laborum(
    parallel: bool = Option(False, "--parallel"),
    not_scraper: bool = Option(False, "--not_scraper"),
    not_clean: bool = Option(False, "--not_clean"),
):
    func = basic_pipeline(
        date, parallel, not_scraper, not_clean
    )
    schedule.every(24).hours.do(func)

    func()
    while True:
        schedule.run_pending()
        time.sleep(1)

#     date = datetime.utcnow().date()

#     scraper = LaborumScraper()
#     scraper.save_all(
#         filter_condition=lambda job: (
#             type(job['published_at']) != datetime or
#             job['published_at'].date() >= date
#         )
#     )

#     db = MongoInterfaces('GetOnBoard')
#     notify_db = MongoInterfaces('NotifyDB')
#     for job in db.all(created_at=date):
#         tjob = GetOnBoardNotifyTransformer(job)

#         if notify_db.exists(id=tjob.id, origin='GetOnBoard'):
#             notify_db.update(tjob.to_dict(), id=tjob.id, origin='GetOnBoard')
#         else:
#             notify_db.insert(tjob.to_dict())

#         print(Logger.format(id=job['id'], title=job['title']))


if __name__ == '__main__':
    app()
