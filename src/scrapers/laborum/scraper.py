from src.python_core.http_scarper import HttpScraper
import os
import requests
import json
import base64

class LaborumScraper(HttpScraper):
    def __init__(self) -> None:
        super().__init__('Laborum')

        self.cookies = os.getenv("Laborum-Cookie")
        self.session  = os.getenv("Laborum-Session") 

    def logger(self, index, job, already):
        print(f"Job {'✅' if already else '🆕'} #{index} ==> {job['titulo']}")


    #############################################
    #                                           #         
    #          Http Configs                     #
    #                                           #
    #############################################

    def __url_compose__(self, n_page = 0, **kwds) -> str:

        return ''.join([
            "https://www.laborum.cl/api/avisos/searchNormalizado?",
            "pageSize=30", # This api has 30 as max page size
            f"&page={n_page}",
            '&sort=fechaOnline%20DESC'
        ])


    @property
    def __headers__(self) -> dict:    
        return {
            'Content-Type':'application/json',
            'Pragma':'no-cache',
            'Accept':'application/json',
            'Host':'www.laborum.cl',
            'Origin':'https://www.laborum.cl',
            'Referer':'https://www.laborum.cl/empleos.html',
            'Connection':'keep-alive',
            'Accept-Language':'en-US,en;q=0.9',
            'Cache-Control':'no-cache',
            'Accept-Encoding':'gzip, deflate, br',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
            'Cookie': self.cookies,
            'x-site-id': 'BMCL',
            'x-session-jwt': self.session
        }


    #############################################
    #                                           #         
    #       Manipulation Config                 #
    #                                           #
    #############################################
    def __job_id__(self, job):
        return {'id': job['id']}
    
    def __get_page__(self, page) -> list[dict]:
        response  = self.post(
            self.__url_compose__(page), 
            body= {
                "filtros":[],
                "busquedaExtendida":True,
                "tipoDetalle":"full",
                "withHome":False,
                "internacional":False
            }
        )

        return response['content']

    def __get_job__(self, job: dict) -> list[dict]:
        response = self.get(f"https://www.laborum.cl/api/candidates/fichaAvisoNormalizada/{job['id']}")
        return job | response