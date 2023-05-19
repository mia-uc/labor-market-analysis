# %%
import requests
import json
from src.etl_process.python_mongo_tools import MongoInterfaces
from datetime import datetime

# %%


def url_compose(offset):
    """
    In GetOnBoard the pagination is 25 for default,
    So the offset should be a multiply of 25

    :param int offset: How many jobs the api have to skip before to count the 25 jobs which will be returned
    """

    return ''.join([
        "https://www.getonbrd.com/webpros/search_jobs.json?",
        f"offset={offset}",
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


def headers_compose(cookies, x_client, x_csrf, x_new_relic):

    return {
        'Cookie': cookies,
        'Pragma': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'www.getonbrd.com',
        'Origin': 'https://www.getonbrd.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://www.getonbrd.com/myjobs',
        'Content-Length': '0',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CLIENT-ID': x_client,
        'X-CSRF-Token': x_csrf,
        'X-NewRelic-ID': x_new_relic
    }

# %%


def jobs(n_page=50, init=0, **config):
    headers = headers_compose(**config)
    base = int(init/25)
    for offset in map(lambda x: x*25, range(base, base + n_page)):
        response = requests.post(url=url_compose(
            offset=offset), data=json.dumps({}), headers=headers)
        res = json.loads(response.content)

        for job in res['jobs']:
            try:
                job['published_at'] = datetime.strptime(
                    job['published_at'], '%b %d').replace(datetime.now().year)
            except:
                pass
            yield job

# %%


JOB_ANALYZED = "Job #{n} ==> {name}"


def find_jobs_and_save(n_page, init, **configs):
    db = MongoInterfaces('GetOnBoard')
    for i, job in enumerate(jobs(n_page, init=init, **configs)):
        job['not_scraped_yet'] = True
        db.insert(job)
        print(JOB_ANALYZED.format(n=i, name=job['title']))


# %%

FIND = '......... Finding jobs from now until {date} ...........'
JOB_ANALYZED_BY_TIME = "Job {date} #{n} ==> {name}"


def find_jobs_until_a_date(date, **configs):
    top = datetime.strptime(date, '%b %d').replace(datetime.now().year)

    print(FIND.format(date=top))

    db = MongoInterfaces('GetOnBoard')
    for i, job in enumerate(jobs(100000, **configs)):
        job['not_scraped_yet'] = True

        if not db.exists(url=job['url']):
            db.insert(job)

        date = job['published_at']
        print(JOB_ANALYZED_BY_TIME.format(n=i, name=job['title'], date=date))
        if date < top and not job['pinned']:
            break
