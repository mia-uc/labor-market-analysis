from src.etl_process.python_mongo_tools import MongoInterfaces
from src.etl_process.jobs_db_center import JobsDBCenter

class GetOnBoardTransformer:
    def __init__(self, job) -> None:
        self.job = job

    def __getattr__(self, __name: str):

        try:
            return self.job[__name]
        except KeyError:
            return None
        

    @property
    def contract(self):
        try:
            if self.job['modality'] == 'Full time':
                return 'full-time'    
            if self.job['modality'] == 'Part time':
                return 'part-time'
            if self.job['modality'] == 'Freelance':
                return 'freelance'
            if self.job['modality'] == 'Internship':
                return 'internship'
        except KeyError:
            pass
        
        return None

    @property
    def modality(self):
        # 'fully_remote', 'hybrid', 'remote_local', 'no_remote', 'temporarily_remote'
        try:
            if self.job['remote_modality'] == 'fully_remote':
                return 'remote'    
            if self.job['remote_modality'] == 'no_remote':
                return 'on-place'

            return 'hybrid'
        except KeyError:
            return None
        
    @property
    def seniority(self):
        # 'Expert','Senior', 'Junior', 'Semi Senior', 'Sin experiencia'
        try:
            if self.job['seniority'] == 'Sin experiencia':
                return 'without-experience'
            if self.job['seniority'] == 'Semi Senior':
                return 'semi-senior'
                        
            return self.job['seniority'].lower()
        except:
            return None

        
    @property
    def hiring_organization(self):
        try:
            return self.job['hiring_company']
        except KeyError:
            pass

        try:
            return self.job['hiring_organization']
        except KeyError:
            pass

        try:
            return self.job['company']['name']
        except Exception:
            pass

        return None

class GetOnBoardCleanPipeline:
    def __init__(self, force = False) -> None:
        self.db = MongoInterfaces('GetOnBoard')
        self.force = force

    def filtered_data(self):
        aggregate = []

        _match = {
            'body': { # If body is defined meats the job was fully scrapped
                '$exists': True
            },
            'job_category' : { # It only matter if is a jobs of IT
                # ITs
                # Programming 
                # Hardware / Electronics 
                # SysAdmin / DevOps / QA 
                # Data Science / Analytics
                # Mobile Development 
                # Sales aprox to Data Science
                # Cybersecurity
                # 
                # Related with ITs 
                # Design / UX => Graphic Design  
                # Operations / Admin => Team Leander  
                # Product, Innovation & Agile => Scrum Master 
                # Content, Advertising & Media == Digital Marketing'
                # Customer Support 
                # People & HR

                '$in': [
                    'Programming',
                    'Hardware / Electronics',
                    'SysAdmin / DevOps / QA',
                    'Data Science / Analytics',
                    'Mobile Development ',
                    'Sales',
                    'Cybersecurity',
                ]
            }
        }

        if not self.force:
            # Take only the data witch have synced yet
            _match['already_fetch'] = {'$exists': False}

        aggregate.append({'$match': _match})
        return self.db.doc.aggregate(aggregate)
    
    def run(self, centered_db: JobsDBCenter):

        for i, job in enumerate(self.filtered_data()):
            transformed_job = GetOnBoardTransformer(job)

            centered_db.migrate(
                _id = transformed_job.id,
                name = transformed_job.title,
                min_salary = transformed_job.min_salary,
                max_salary = transformed_job.max_salary,
                seniority = transformed_job.seniority,
                work_modality = transformed_job.modality,
                contract_type = transformed_job.contract,
                published_at = transformed_job.published_at,
                hiring_organization = transformed_job.hiring_organization,
                description = transformed_job.body,
                country = transformed_job.country,
                city = transformed_job.city,
                origin = 'GetOnBoard',
                currency = 'usd'
            )

            print(f"..... Cleaning the job #{i} => {transformed_job.id} => {transformed_job.title}")

            self.db.update({'already_fetch': True}, **{'id': job['id'], 'url': job['url']})
    



