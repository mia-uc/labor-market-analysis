# %%

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
from functools import partial
from src.etl_process.python_mongo_tools import MongoInterfaces

def find_details_for_new_job():
    # exe = ThreadPoolExecutor()
    db = MongoInterfaces('GetOnBoard')

    # thread = exe.map(partial(get_details_for_job, db = db), db.all(not_scraped_yet = True))

    # return list(thread)

    for job in db.all(not_scraped_yet = True):
        get_details_for_job(job, db)

def get_details_for_job(job: dict, db: MongoInterfaces):
    print(f"🪲 GetOnBoard Scraper are Finding Details for {job['id']} - {job['title']}")
    page = requests.get('https://www.getonbrd.com/' + job['url']).content
    soup = BeautifulSoup(page, 'html.parser')   

    new_info = {}

    body = soup.find("div", {"id": "job-body", "itemprop": 'description'})
    new_info['body'] = body.get_text().strip()

    apply_bottom = soup.find("a", {"id": "apply_bottom"})
    new_info["url_to_apply"] = apply_bottom.get('href')

    quick_apply_bottom = soup.find("a", {"id": "quick_apply_bottom"})
    new_info["url_to_apply_quick"] = None if quick_apply_bottom is None else quick_apply_bottom.get('href')
    
    tags = soup.find('div', {"class":"gb-tags", "itemprop":"skills"})
    if tags:
        new_info["jobs_tags"] = [a.get_text().strip() for a in tags.find_all('a')]

    header = soup.find('div', {'class': 'gb-company-theme-colored'})
    if header and (applications := header.find('div', {'class': 'size0 mt1'})):
        text = applications.get_text()
        
        if (match := re.search(r'\d+\s*applications', text.strip())):
            new_info["n_applications"] = match.group().replace('\n', ' ').strip()

        if (match := re.search(r'Requires\s*applying\s*in\s*\w+', text)):
            new_info["language_application_required"] = match.group()

    new_info['not_scraped_yet'] = False

    return db.update(new_info, url = job['url'], id = job['id'], _id = job['_id'])


# %%
