import requests
import json
from src.etl_process.python_mongo_tools import MongoInterfaces
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from logging import warn

class HttpScraper:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self.db = MongoInterfaces(db_name)

    def logger(self, index, job, already):
        return 
    
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
    

    def __save__(self, index, job, check = True):
        already = self.db.exists( **self.__job_id__(job))
        self.logger(index, job, already)

        if not check or not already:
            try:
                job = self.__get_job__(job)
                if job:
                    self.db.insert(job)
            except json.JSONDecodeError:
                warn("There were an error")

        return job

    def __get_page__(self, page) -> list[dict]:
        """"""

    def __get_job__(self, job: dict) -> list[dict]:
        job['not_scraped_yet'] = True
        return job

    @property
    def http_client(self):
        if hasattr(self, 'session'):
            return self.session
        
        return requests

    def post(self, url, body = {}) -> dict:
        response = self.http_client.post(
            url=url, 
            data=json.dumps(body), 
            headers=self.__headers__
        )

        try:
            return json.loads(response.content)
        except json.JSONDecodeError as e:
            print(response.content)

            raise e
    
    def get(self, url) -> dict:
        response = self.http_client.get(
            url=url, 
            headers=self.__headers__
        )

        try:
            return json.loads(response.content)
        except json.JSONDecodeError as e:
            print(response.content)

            raise e

    def save_all(self, n_page = -1, skips = 0, filter_condition = lambda j: True, parallel = False):
        print(f'....... Downloading all jobs in {self.db_name} 🤑')
        exe = ThreadPoolExecutor()
        page, index = skips, 0

        try:
            while True:
                jobs = self.__get_page__(page)

                # Use filter condition to control the stop conditions
                # If any jobs complies with the condition the loop would stop
                jobs = [j for j in jobs if filter_condition(j)]

                if len(jobs) == 0 or page == n_page:
                    break
                
                if parallel:
                    print(parallel)
                    list(exe.map(
                        self.__save__,
                        range(index, index + len(jobs)),
                        jobs
                    ))
                else:
                    for i, j in zip(range(index, index + len(jobs)), jobs):
                        self.__save__(i, j) 

                page += 1
                index += len(jobs)
        
        except KeyboardInterrupt:
            pass
        except ConnectionError:
            pass
        
        print(f'....... The {self.db_name} scraper has finished, {page - skips} pages and {index} jobs have been viewed')

    def update(self, parallel = False, force = False):
        print(f'....... Updating jobs in {self.db_name}')
        exe = ThreadPoolExecutor()

        def f(info):
            index, job = info
            response = self.__get_job__(job)
            self.logger(index, job, True)

            if response:
                response['not_scraped_yet'] = False

                if '_id' in response:
                    del response['_id']

                keys = self.__job_id__(job)

                if not force:
                    keys['not_scraped_yet'] = True

                self.db.update(response, **keys)

        conditions = {}

        if not force:
            conditions['not_scraped_yet'] = True

        if parallel:
            return list(exe.map(
                f,  enumerate(self.db.all(**conditions))
            ))

        for info in enumerate(self.db.all(**conditions)):

            try:
                f(info)
            except json.JSONDecodeError:
                pass