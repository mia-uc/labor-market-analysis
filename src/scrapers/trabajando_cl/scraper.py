from src.python_core.http_scarper import HttpScraper
import os
import requests
import json
import base64

class WorkingCLScraper(HttpScraper):
    def __init__(self) -> None:
        super().__init__(
            'Trabajando.cl', 
            'ofertas', 
            self.logger
        )

        self.cookie = os.getenv("TrabajandoCL-Cookie")

    def logger(self, index, job):
        print(f"Job #{index} ==> {job['cargo']}")


    #############################################
    #                                           #         
    #          Http Configs                     #
    #                                           #
    #############################################

    def __url_compose__(self, n_page = 0, **kwds) -> str:

        return ''.join([
            "https://www.trabajando.cl/api/searchjob?",
            f"Pagina={n_page}",
            "&AliasOrden=5",
            "&TextoLibre",
            "&IDEmpresas",
            "&avisoconfidencial",
        ])


    @property
    def __headers__(self) -> dict:    
        return {
            'Accept':'*/*',
            'Pragma':'no-cache',
            'Host':'www.trabajando.cl',
            'Referer':'https://www.trabajando.cl/trabajo-empleo/?ubicacion=chile',
            'Connection':'keep-alive',
            'Cache-Control':'no-cache',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
            'Accept-Language':'en-US,en;q=0.9',
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
    
    def requests(self, page) -> dict:
        response = requests.get(
            url=self.__url_compose__(n_page = page), 
            headers=self.__headers__
        )
        
        res = json.loads(response.content)
        return res[self.list_name]
