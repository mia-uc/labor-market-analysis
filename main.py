from typer import Typer
from src.scrapers import getonboard as getonbrd
from src.scrapers import laborum as laborum
from src.scrapers import trabajando_cl
from dotenv import load_dotenv

load_dotenv()
app = Typer()

getonbrd.commands(app)
laborum.commands(app)
trabajando_cl.commands(app)

if __name__ == "__main__":
    app()