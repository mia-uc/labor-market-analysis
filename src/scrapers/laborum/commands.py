
from typer import Typer, Option
from .scraper import LaborumScraper

# Reference https://www.laborum.cl

def commands(app: Typer):
    
    @app.command()
    def laborum(n_page: int = -1, offset: int = 0, date: str = None, parallel : bool = Option(False, "--parallel")):
        scraper = LaborumScraper()

        # params = {}
        # if date:
        #     params
    
        return scraper.save_all(
            n_page=n_page,
            skips=offset,
            parallel = parallel
        )

    @app.command()
    def update_laborum(parallel : bool = Option(False, "--parallel")):
        scraper = LaborumScraper()

        return scraper.update(parallel)

    # @app.command()
    # def getonbrd_update():
    #     return find_details_for_new_job()