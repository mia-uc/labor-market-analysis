from typer import Typer
from src.scrapers import getonboard as GetOnBoard
import configparser
from dotenv import load_dotenv
import os

load_dotenv()
app = Typer()

@app.command()
def getonbrd(n_page: int, offset: int = 0):
    GetOnBoard.find_jobs_and_save(
        n_page, offset,
        cookies = os.getenv("GetOnBoard-Cookie"), 
        x_client  = os.getenv("GetOnBoard-X-CLIENT-ID"), 
        x_csrf = os.getenv("GetOnBoard-X-CSRF-Token"), 
        x_new_relic  = os.getenv("GetOnBoard-X-NewRelic-ID"), 
    )

@app.command()
def getonbrd_by_date(date: str):
    GetOnBoard.find_jobs_until_a_date(
        date,
        cookies = os.getenv("GetOnBoard-Cookie"), 
        x_client  = os.getenv("GetOnBoard-X-CLIENT-ID"), 
        x_csrf = os.getenv("GetOnBoard-X-CSRF-Token"), 
        x_new_relic  = os.getenv("GetOnBoard-X-NewRelic-ID"), 
    )

@app.command()
def getonbrd_update():
    return GetOnBoard.find_details_for_new_job()

if __name__ == "__main__":
    app()