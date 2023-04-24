
from typer import Typer
from .find_jobs import find_jobs_and_save, find_jobs_until_a_date
from .find_details import find_details_for_new_job
import os


# Reference https://www.getonboard.com

def commands(app: Typer):
    @app.command()
    def getonbrd(n_page: int, offset: int = 0):
        find_jobs_and_save(
            n_page, offset,
            cookies = os.getenv("GetOnBoard-Cookie"), 
            x_client  = os.getenv("GetOnBoard-X-CLIENT-ID"), 
            x_csrf = os.getenv("GetOnBoard-X-CSRF-Token"), 
            x_new_relic  = os.getenv("GetOnBoard-X-NewRelic-ID"), 
        )

    @app.command()
    def getonbrd_by_date(date: str):
        find_jobs_until_a_date(
            date,
            cookies = os.getenv("GetOnBoard-Cookie"), 
            x_client  = os.getenv("GetOnBoard-X-CLIENT-ID"), 
            x_csrf = os.getenv("GetOnBoard-X-CSRF-Token"), 
            x_new_relic  = os.getenv("GetOnBoard-X-NewRelic-ID"), 
        )

    @app.command()
    def getonbrd_update():
        return find_details_for_new_job()