from typer import Typer
from src.scrapers import getonboard as getonbrd
from src.scrapers import laborum as laborum
from src.scrapers import trabajando_cl
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()
app = Typer()

getonbrd.commands(app)
laborum.commands(app)
trabajando_cl.commands(app)


@app.command()
def mongo_migrate():

    connection_string =  os.getenv("MONGO_CONN_STRING")
    db_name = os.getenv('MONGO_DB')


    # Conexión con la instancia de Origen
    origen_cliente = MongoClient(connection_string)
    origen_db = origen_cliente[db_name]


    des_connection_string =  os.getenv("DESTINO_MONGO_CONN_STRING")
    # Conexión con la instancia de Destino
    destino_cliente = MongoClient(des_connection_string)
    destino_db = destino_cliente[db_name]

    for collection in ['Laborum', 'Trabajando.cl']:
        print(f'------------------- {collection} --------------------------')

        origen_collection = origen_db[collection]
        destino_collection = destino_db[collection]
        # Copiar los datos de la colección desde origen a destino
        for i, documento in enumerate(origen_collection.find()):
            print(f'------------------- {i} --------------------------', end='\r')
            destino_collection.insert_one(documento)

if __name__ == "__main__":
    app()