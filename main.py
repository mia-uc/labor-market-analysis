from typer import Typer
from src.scrapers import getonboard as getonbrd
from src.scrapers import laborum as laborum
from src.scrapers import trabajando_cl
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
app = Typer()

getonbrd.commands(app)
laborum.commands(app)
trabajando_cl.commands(app)


@app.command()
def mongo_migrate():

    # Conexión con la instancia de Origen
    origen_cliente = MongoClient('mongodb://<usuario>:<password>@<servidor_origen>:<puerto_origen>')
    origen_db = origen_cliente['<nombre_de_la_db_origen>']
    origen_coleccion = origen_db['<nombre_de_la_coleccion_origen>']
    
    # Conexión con la instancia de Destino
    destino_cliente = MongoClient('mongodb://<usuario>:<password>@<servidor_destino>:<puerto_destino>')
    destino_db = destino_cliente['<nombre_de_la_db_destino>']
    destino_coleccion = destino_db['<nombre_de_la_coleccion_destino>']
    
    # Copiar los datos de la colección desde origen a destino
    for documento in origen_coleccion.find():
        destino_coleccion.insert_one(documento)

if __name__ == "__main__":
    app()