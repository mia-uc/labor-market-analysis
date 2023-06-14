from typer import Option, Typer
from datetime import datetime
from scrapers.getonboard import pipelines as GetOnBoardPipeline
from scrapers.laborum import pipelines as LaborumPipeline
from scrapers.trabajando_cl import pipelines as WorkingClPipeline
from dotenv import load_dotenv

import schedule
import time


load_dotenv()
app = Typer()


def cronjob(func):
    schedule.every(24).hours.do(func)

    func()
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.command()
def getonbrd(
    parallel: bool = Option(False, "--parallel"),
    not_scraper: bool = Option(False, "--not_scraper"),
    not_clean: bool = Option(False, "--not_clean"),
):
    func = GetOnBoardPipeline.basic_pipeline(
        parallel, not_scraper, not_clean
    )

    cronjob(func)


@app.command()
def laborum(
    parallel: bool = Option(False, "--parallel"),
    not_scraper: bool = Option(False, "--not_scraper"),
    not_clean: bool = Option(False, "--not_clean"),
):
    func = LaborumPipeline.basic_pipeline(
        parallel, not_scraper, not_clean)

    cronjob(func)


@app.command()
def working_cl(
    parallel: bool = Option(False, "--parallel"),
    not_scraper: bool = Option(False, "--not_scraper"),
    not_clean: bool = Option(False, "--not_clean"),
):
    func = WorkingClPipeline.basic_pipeline(
        parallel, not_scraper, not_clean)

    cronjob(func)


if __name__ == '__main__':
    app()
