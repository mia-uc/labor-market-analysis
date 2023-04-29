from src.python_core.http_scarper import HttpScraper
import os
import requests
import json
import base64
from datetime import datetime
from bs4 import BeautifulSoup
import re


# References http://trabajando.cl

class GetOnBoardScraper(HttpScraper):
    def __init__(self) -> None:
        super().__init__('GetOnBoard')

        self.cookies = os.getenv("GetOnBoard-Cookie")
        self.x_client  = os.getenv("GetOnBoard-X-CLIENT-ID")
        self.x_csrf = os.getenv("GetOnBoard-X-CSRF-Token")
        self.x_new_relic  = os.getenv("GetOnBoard-X-NewRelic-ID") 

    def logger(self, index, job, already):
        print(f"From {job['published_at']} Job {'✅' if already else '🆕'} #{index} ==> {job['title']}")


    #############################################
    #                                           #         
    #          Http Configs                     #
    #                                           #
    #############################################

    def __url_compose__(self, n_page = 0, **kwds) -> str:
        return ''.join([
            "https://www.getonbrd.com/webpros/search_jobs.json?",
            f"offset={n_page * 25}",
            "&tags_criteria=any",
            "&webpro%5Bcategory_ids%5D%5B%5D=",
            "&webpro%5Btag_ids%5D%5B%5D=",
            "&webpro%5Bmodality_ids%5D%5B%5D=",
            "&webpro%5Btenant_ids%5D%5B%5D=",
            "&webpro%5Bseniority_ids%5D%5B%5D=",
            "&webpro%5Bcompanies_blacklist_ids%5D%5B%5D=",
            "&webpro%5Bremote_jobs%5D=false",
            "&webpro%5Bmin_salary%5D=0",
        ])


    @property
    def __headers__(self) -> dict:    
        return {
            'Cookie': self.cookies,
            'Pragma':'no-cache',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Language':'en-US,en;q=0.9',
            'Cache-Control':'no-cache',
            'Accept-Encoding':'gzip, deflate, br',
            'Host':'www.getonbrd.com',
            'Origin':'https://www.getonbrd.com',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
            'Connection':'keep-alive',
            'Referer':'https://www.getonbrd.com/myjobs',
            'Content-Length':'0',
            'X-Requested-With':'XMLHttpRequest',
            'X-CLIENT-ID': self.x_client,
            'X-CSRF-Token': self.x_csrf,
            'X-NewRelic-ID': self.x_new_relic
        }


    #############################################
    #                                           #         
    #       Manipulation Config                 #
    #                                           #
    #############################################
    def __job_id__(self, job):
        return {'url': job['url'], 'id': job['id']}
    
    def __get_page__(self, page) -> list[dict]:
        response  = self.post(self.__url_compose__(page))

        for job in response['jobs']:
            job['published_at'] = datetime.strptime(job['published_at'], '%b %d').replace(datetime.now().year)
        
        return response['jobs']

    def __get_job__(self, job: dict) -> list[dict]:

        print(f"🪲 GetOnBoard Scraper are Finding Details for {job['id']} - {job['title']}")
        page = requests.get('https://www.getonbrd.com/' + job['url']).content
        soup = BeautifulSoup(page, 'html.parser')   

        new_info = {}

        if (body := soup.find("div", {"id": "job-body", "itemprop": 'description'})):
            new_info['body'] = body.get_text().strip()

        if (apply_bottom := soup.find("a", {"id": "apply_bottom"})):
            new_info["url_to_apply"] = apply_bottom.get('href')

        if (quick_apply_bottom := soup.find("a", {"id": "quick_apply_bottom"})):
            new_info["url_to_apply_quick"] = quick_apply_bottom.get('href')


        if (tags := soup.find('div', {"itemprop":"skills"})):
            new_info["jobs_tags"] = [a.get_text().strip() for a in tags.find_all('a')]

        header = soup.find('div', {'class': 'gb-company-theme-colored'})
        if header and (applications := header.find('div', {'class': 'size0 mt1'})):
            text = applications.get_text()

            if (match := re.search(r'\d+\s*applications', text.strip())):
                new_info["n_applications"] = match.group().replace('\n', ' ').strip()

            if (match := re.search(r'Requires\s*applying\s*in\s*\w+', text)):
                new_info["language_application_required"] = match.group()
        
        if (span := soup.find('span', {"itemprop":"qualifications"})):
            if (job_category := span.find_next_sibling('a')):
                new_info['job_category'] = job_category.text.strip()

        return job | new_info