from typer import Typer
import src.scrapers.getonboard as getonbrd
import src.scrapers.laborum as laborum
from dotenv import load_dotenv

load_dotenv()
app = Typer()

getonbrd.commands(app)
laborum.commands(app)

if __name__ == "__main__":
    app()