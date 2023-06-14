from scrapers.http_scarper import HttpScraper
import os
import requests
import json
import base64
from datetime import datetime, timedelta
import re
from logging import warn
# References http://trabajando.cl


class WorkingCLScraper(HttpScraper):
    def __init__(self) -> None:
        super().__init__('Trabajando.cl')

        self.cookie = os.getenv("TrabajandoCL-Cookie")

    def logger(self, index, job, already):
        print(
            f"From {job['published_at']} Job {'✅' if already else '🆕'} #{index} ==> {job['nombreCargo']}")

    #############################################
    #                                           #
    #          Http Configs                     #
    #                                           #
    #############################################

    def __url_compose__(self, n_page=0, **kwds) -> str:

        return ''.join([
            "https://www.trabajando.cl/api/searchjob?",
            f"Pagina={n_page}",
            "&AliasOrden=3",
            "&TextoLibre",
            "&IDEmpresas",
            "&avisoconfidencial",
        ])

    @property
    def __headers__(self) -> dict:
        return {
            'Accept': '*/*',
            'Pragma': 'no-cache',
            'Host': 'www.trabajando.cl',
            'Referer': 'https://www.trabajando.cl/trabajo-empleo/?ubicacion=chile',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
            'Accept-Language': 'en-US,en;q=0.9',
            # 'Accept-Encoding':'gzip, deflate, br',
            'Cookie': self.cookie
        }

    #############################################
    #                                           #
    #       Manipulation Config                 #
    #                                           #
    #############################################

    def __job_id__(self, job):
        return {'idOferta': job['idOferta']}

    def __get_page__(self, page) -> list[dict]:
        response = self.get(self.__url_compose__(page))

        base_date = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        for job in response['ofertas']:
            try:
                job['published_at'] = job['fechaPublicacion'].strip()
            except KeyError:
                job['published_at'] = job['publicadoHace'].strip()

            if 'publicada hoy' in job['published_at'].lower():
                job['published_at'] = base_date

            elif 'publicada ayer' in job['published_at'].lower():
                job['published_at'] = base_date \
                    - timedelta(days=1)

            elif (match := re.search(
                r'hace\s+(?P<days>\d+)\s+días',
                job['published_at'], re.IGNORECASE)
            ):
                job['published_at'] = base_date \
                    - timedelta(days=int(match.group('days')))

            else:
                try:
                    job['published_at'] = datetime.strptime(
                        job['published_at'], '%d/%m/%Y').\
                        replace(datetime.now().year)
                except:
                    warn("Published at wasn't detected")

        return response['ofertas']

    def __get_job__(self, job: dict) -> list[dict]:
        response = self.get(
            f"https://www.trabajando.cl/api/ofertas/{job['idOferta']}")
        return job | response
