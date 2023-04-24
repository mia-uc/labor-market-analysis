from typer import Typer
from .scraper import WorkingCLScraper
# from .find_details import find_details_for_new_job
import os

# Reference https://www.laborum.cl

def commands(app: Typer):
    @app.command()
    def trabajando_cl(n_page: int = -1, offset: int = 0, date: str = None):
        scraper = WorkingCLScraper()

        # params = {}
        # if date:
        #     params

        return scraper.save_all(
            n_page=n_page,
            skips=offset,
        )

