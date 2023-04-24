import requests
import json
from src.etl_process.python_mongo_tools import MongoInterfaces
from concurrent.futures import ThreadPoolExecutor

class HttpScraper:
    def __init__(self, db_name, list_name, logger) -> None:
        self.db_name = db_name
        self.db = MongoInterfaces(db_name)
        self.list_name = list_name
        self.logger = logger

    #############################################
    #                                           #         
    #          Http Configs                     #
    #                                           #
    #############################################

    def __url_compose__(self, n_page = 0, **kwds) -> str:
        """"""

    @property
    def __headers__(self) -> dict:
        """"""
        
        return {}

    def __body__(self, n_page = 0, **kwds) -> dict:
        """"""

        return {}
    

    #############################################
    #                                           #         
    #       Manipulation Config                 #
    #                                           #
    #############################################
    def __job_id__(self, job):
        return {'id': job['id']}
    

    def __save__(self, index, job):
        self.logger(index, job)

        job['not_scraped_yet'] = True
        if not self.db.exists( **self.__job_id__(job) ):
            self.db.insert(job)

        return job

    def requests(self, page) -> dict:
        response = requests.post(
            url=self.__url_compose__(n_page = page), 
            data=json.dumps(self.__body__()), 
            headers=self.__headers__
        )

        res = json.loads(response.content)
        
        return res[self.list_name]

    def save_all(self, n_page = -1, skips = 0, filter_condition = lambda j: True):
        print(f'....... Downloading all jobs in {self.db_name} 🤑')
        exe = ThreadPoolExecutor()
        page, index = skips, 0

        try:
            while True:
                jobs = self.requests(page)

                # Use filter condition to control the stop conditions
                # If any jobs complies with the condition the loop would stop
                jobs = [j for j in jobs if filter_condition(j)]

                if len(jobs) == 0 or page == n_page:
                    break

                list(exe.map(
                    self.__save__,
                    range(index, index + len(jobs)),
                    jobs
                ))

                page += 1
                index += len(jobs)
        
        except KeyboardInterrupt:
            pass
        
        print(f'....... The {self.db_name} scraper has finished, {page - skips} pages and {index} jobs have been viewed')

