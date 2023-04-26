
from typer import Option, Typer
import os

from .scraper import GetOnBoardScraper


# Reference https://www.getonboard.com
    


def commands(app: Typer):
    
    @app.command()
    def getonbrd(n_page: int = -1, offset: int = 0, date: str = None, parallel : bool = Option(False, "--parallel")):
        scraper = GetOnBoardScraper()

        # params = {}
        # if date:
        #     params
    
        return scraper.save_all(
            n_page=n_page,
            skips=offset,
            parallel = parallel
        )

    @app.command()
    def update_getonbrd(parallel : bool = Option(False, "--parallel"), force : bool = Option(False, "--force")):
        scraper = GetOnBoardScraper()

        return scraper.update(parallel, force)