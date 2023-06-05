from src.python_core.http_scarper import HttpScraper
import os
import requests
import json
import base64
from datetime import datetime
from bs4 import BeautifulSoup
import re


# References http://trabajando.cl

class ChileWorks(HttpScraper):
    def __init__(self) -> None:
        super().__init__('ChileTrabajo')

    def logger(self, index, job, already):
        print(
            f"From {job['date']} Job {'✅' if already else '🆕'} #{index} ==> {job['title']}")

    #############################################
    #                                           #
    #          Http Configs                     #
    #                                           #
    #############################################

    def __url_compose__(self, n_page=0, **kwds) -> str:
        if n_page:
            return f'https://www.chiletrabajos.cl/encuentra-un-empleo/{n_page*30}'

        return f'https://www.chiletrabajos.cl/encuentra-un-empleo?'

    #############################################
    #                                           #
    #       Manipulation Config                 #
    #                                           #
    #############################################

    def __job_id__(self, job):
        return {'url': job['url']}

    def __get_page__(self, page) -> list[dict]:
        response = self.get(self.__url_compose__(page), json_load=False)
        soup = BeautifulSoup(response, 'html.parser')

        jobs = []
        for link in soup.find_all('div', {'class': 'job-item'}):
            j = {
                'title': link.h2.get_text().strip(),
                'url': link.h2.a.get('href')
            }

            h3s = link.find_all('h3')
            j['date'] = h3s[1].get_text().strip()
            jobs.append(j)

        return jobs

    def __get_job__(self, job: dict) -> list[dict]:

        print(f"🪲 ChileTrabajo Scraper are Finding Details for {job['title']}")
        page = requests.get(job['url']).content
        soup = BeautifulSoup(page, 'html.parser')

        new_info = {
            "title": soup.h1.get_text(),
        }

        table = soup.tbody
        for tr in table.find_all('tr'):
            field = [td.get_text().strip() for td in tr.find_all('td')]
            if len(field) == 2:
                new_info[field[0]] = field[1]

        div = soup.find('div', {'class': 'job-item'})
        ps = div.find_all(
            'p',
            string=lambda text: not text or 'PUBLICIDAD' not in text
        )

        new_info['description'] = ps[0].get_text()

        if len(ps) > 0:
            for i in range(1, len(ps)):
                new_info[f'description{i}'] = ps[i].get_text()

        return job | new_info
