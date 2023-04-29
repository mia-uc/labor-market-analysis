from src.etl_process.python_mongo_tools import MongoInterfaces
from datetime import datetime

class JobsDBCenter:
    def __init__(self) -> None:
        self.db = MongoInterfaces('CleanJobs')
    
    def migrate(
        self,
        _id : str,
        name : str,
        origin : str,
        min_salary : float = None,
        max_salary : float = None,
        currency: str = None,
        seniority : str = None,
        work_modality : str = None,
        contract_type : str = None,
        published_at : datetime.datetime = None,
        hiring_organization : str = None,
        description : str = None,
        country : str = None,
        city : str = None,
    ):
        
        assert _id
        assert name and type(name) == str
        assert origin in ['GetOnBoard']

        if min_salary or max_salary:
            assert currency in ['usd']
            assert not min_salary or (type(min_salary) in [int, float] and min_salary >= 0)
            assert not max_salary or (type(max_salary) in [int, float] and max_salary >= 0)
        

        assert not seniority or seniority in ['senior', 'semi-senior', 'without-experience', 'junior', 'expert']
        assert not work_modality or work_modality in ['hybrid', 'on-place', 'remote']
        assert not contract_type or contract_type in ['full-time', 'part-time', 'freelance', 'internship']
        assert not hiring_organization or type(hiring_organization) == str
        assert not description or type(description) == str
        assert not country or type(country) == str
        assert not city or type(city) == str

        body = {
            'id' : _id,
            'name' : name,
            'origin' : origin,
            'min_salary' : min_salary,
            'max_salary' : max_salary,
            'currency' : currency,
            'seniority' : seniority,
            'work_modality' : work_modality,
            'contract_type' : contract_type,
            'published_at' : published_at,
            'hiring_organization' : hiring_organization,
            'description' : description,
            'country' : country,
            'city' : city,
        }

        self.db.update(body, {'id': _id, 'origin': origin})