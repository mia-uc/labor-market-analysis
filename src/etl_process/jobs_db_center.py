
from src.etl_process.python_mongo_tools import MongoInterfaces
from datetime import datetime

from concurrent.futures import ThreadPoolExecutor
from .text_entities_detection import build_language_programming_detector, build_skills_detector, llm_predict
import openai
import os


class JobsDBCenter:
    def __init__(self, name='CleanITJobs', check_llm=False) -> None:
        self.db = MongoInterfaces(name)
        self.exe = ThreadPoolExecutor()

        self.lp_detector = build_language_programming_detector()
        self.skill_detector = build_skills_detector()

        self.check_llm = check_llm
        if self.check_llm:
            openai.api_key = os.getenv("OPEN_AI_API_KEY")

    def migrate(
        self,
        _id: str,
        name: str,
        origin: str,
        min_salary: float = None,
        max_salary: float = None,
        currency: str = None,
        seniority: str = None,
        work_modality: str = None,
        contract_type: str = None,
        published_at: datetime = None,
        hiring_organization: str = None,
        description: str = None,
        country: str = None,
        city: str = None,
        programming_languages: list = [],
        jobs_category=None
    ):

        assert _id
        assert name and type(name) == str
        assert origin in ['GetOnBoard', 'Laborum', 'Trabajando.cl']

        if min_salary or max_salary:
            assert currency in ['usd', 'clp']
            assert not min_salary or (
                type(min_salary) in [int, float] and min_salary >= 0)
            assert not max_salary or (
                type(max_salary) in [int, float] and max_salary >= 0)

        assert not seniority or seniority in [
            'senior', 'semi-senior', 'without-experience', 'junior', 'expert']
        assert not work_modality or work_modality in [
            'hybrid', 'on-place', 'remote']
        assert not contract_type or contract_type in [
            'full-time', 'part-time', 'freelance', 'internship', 'per-hours', 'weekends', 'at-night', 'in-turns']
        assert not hiring_organization or type(hiring_organization) == str
        assert not description or type(description) == str
        assert not country or type(country) == str
        assert not city or type(city) == str

        assert type(programming_languages) == list
        assert not jobs_category or jobs_category in [
            'back-end', 'front-end', 'full-stack']

        body = {
            'id': _id,
            'name': name,
            'origin': origin,
            'min_salary': min_salary,
            'max_salary': max_salary,
            'currency': currency,
            'seniority': seniority,
            'work_modality': work_modality,
            'contract_type': contract_type,
            'published_at': published_at,
            'hiring_organization': hiring_organization,
            'description': description,
            'country': country,
            'city': city,
            'programming_languages': programming_languages,
            'jobs_category': jobs_category
        }

        body |= self.body_update(body)

        if self.check_llm:
            body |= self.llm_analyze(body)

        if self.db.exists(id=_id, origin=origin):
            self.db.update(body, id=_id, origin=origin)
        else:
            self.db.insert(body)

    def body_update(self, job):

        new_info = {}

        # titles = job_detector(job['name'])
        # if titles:
        #     new_info['job_type'] = titles
        # print(f"\t{titles}")
        text = f"{job['name']}\n{job['description']}"
        new_info['lps'] = self.lp_detector(text, self.exe)

        new_info['skills'] = self.skill_detector(text, self.exe)

        return new_info
        # self.db.update(new_info, id=job['id'], origin=job['origin'])

    def llm_analyze(self, job):
        s = '0-'
        for _ in range(5):
            s += llm_predict(job['description'], s)
            s += '\n'

        return {'openai-text': s}


# !rm -r labor-market-analysis
# !git clone https://github.com/mia-uc/labor-market-analysis.git
# %cd labor-market-analysis

# !pip install -r requirements.txt
# !pip install pandas fuzzywuzzy python-Levenshtein


# from src.etl_process.python_mongo_tools import MongoInterfaces
# from src.etl_process.jobs_db_center import JobsDBCenter
# import pymongo
# import os

# os.environ['MONGO_CONN_STRING'] = 'mongodb+srv://DataScienceTeam:rNA6xe4OU7cvv8it@jobsdatalake.goyvrjl.mongodb.net/?retryWrites=true&w=majority'
# os.environ['MONGO_DB'] = 'jobs'
# db = MongoInterfaces("CleanITJobs")
# center = JobsDBCenter()
# for i, job in enumerate(db.all(skills={'$exists': False}, sort=[('name', pymongo.DESCENDING)])):
#     new_info = center.body_update(job)
#     db.update(new_info, id=job['id'], origin=job['origin'])
