# %%
import requests
import json
from src.etl_process.python_mongo_tools import MongoInterfaces
from datetime import datetime

# %%

def url_compose(page):
    """
    :param int offset: How many page the api have to skip before to count the 30 jobs which will be returned
    """
    'https://www.laborum.cl/api/avisos/searchNormalizado?pageSize=100&page=0'
    return ''.join([
        "https://www.laborum.cl/api/avisos/searchNormalizado?",
        "pageSize=30", # This api has 30 as max page size
        f"&page={page}",
        '&sort=fechaOnline%20DESC'
    ])

def headers_compose(cookies, session):

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
        'Cookie': cookies,
        'x-site-id': 'BMCL',
        'x-session-jwt': session, 
    }

def body():
    return {
        "filtros":[],
        "busquedaExtendida":True,
        "tipoDetalle":"full",
        "withHome":False,
        "internacional":False
    }


def jobs(n_page = 50, base = 0, **config):
    headers = headers_compose(**config)
    for page in range(base, base + n_page):
        response = requests.post(url=url_compose(page = page), data=json.dumps(body()), headers=headers)
        res = json.loads(response.content)

        for job in res['content']:
            yield job


def find_jobs_and_save(n_page, init, **configs):
    db = MongoInterfaces('Laborum')
    for i, job in enumerate(jobs(n_page, init, **configs)):
        
        job['not_scraped_yet'] = True
        db.insert(job)

        print(f"Job #{i} ==> {job['titulo']}")
        

# %%

FIND = '......... Finding jobs from now until {date} ...........'
JOB_ANALYZED_BY_TIME = "Job {date} #{n} ==> {name}"

def find_jobs_until_a_date(date, **configs):
    db = MongoInterfaces('Laborum')

    top = datetime.strptime(date, '%b %d').replace(datetime.now().year)
    
    print(FIND.format(date = top))

    for i, job in enumerate(jobs(100000, **configs)):
        job['not_scraped_yet'] = True

        if not db.exists(id = job['id']):
            db.insert(job)

        date = job['fechaHoraPublicacion']
        print(JOB_ANALYZED_BY_TIME.format(n=i, name = job['titulo'], date = date))
        if date < top:
            break