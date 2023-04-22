
from typer import Typer
from .find_jobs import find_jobs_and_save, find_jobs_until_a_date
# from .find_details import find_details_for_new_job
import os

def commands(app: Typer):
    @app.command()
    def laborum(n_page: int, offset: int = 0):
        find_jobs_and_save(
            n_page, offset,
            cookies = os.getenv("Laborum-Cookie"), 
            session  = os.getenv("Laborum-Session"), 
        )

    @app.command()
    def laborum_by_date(date: str):
        find_jobs_until_a_date(
            date,
            cookies = os.getenv("Laborum-Cookie"), 
            session  = os.getenv("Laborum-Session"), 
        )

    # @app.command()
    # def getonbrd_update():
    #     return find_details_for_new_job()