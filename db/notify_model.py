from .python_mongo_tools import MongoInterfaces


class NotifyModel(MongoInterfaces):
    def __init__(self) -> None:
        super().__init__("NotifyDB")

    def save(self, job):
        body = {
            "id": job.id,
            "name": job.title,
            'min_salary': job.min_salary,
            'max_salary': job.max_salary,
            'experience': job.seniority,
            'work_modality': job.modality,
            'contract_type': job.contract,
            'published_at': job.published_at,
            'hiring_organization': job.hiring_organization,
            'description': job.body,
            'country': job.country,
            'city': job.city,
            'origin': job.origin,
            'currency': job.currency,
            'url': job.url,
            'sms': self.build_sms(job)
        }

        if self.exists(id=job.id, origin=job.currency):
            self.update(body, id=job.id, origin=job.currency)
        else:
            self.insert(body)

    def build_sms(self, job):
        sms = f'{job.title}\n'

        if job.hiring_organization:
            sms = f'🏢 {job.hiring_organization} \n'

        if job.min_salary or job.max_salary:
            if (
                job.min_salary and job.max_salary and
                job.min_salary != job.max_salary
            ):
                sms += f'💰 {job.min_salary} - {job.max_salary} {job.currency}\n'
            elif job.min_salary:
                sms += f'💰 {job.min_salary} {job.currency}\n'
            else:
                sms += f'💰 {job.max_salary} {job.currency}\n'

        sms += '\n\n'
        add_line = False

        from_ = list(filter(lambda x: x, [job.city, job.country, job.origin]))
        if from_:
            add_line = True
            sms += f'🌎 {from_[0]}'
            for t in from_[1:]:
                sms += f' / {t}'

            sms += '\n'

        details = list(filter(lambda x: x, [
            job.seniority, job.modality, job.contract
        ]))

        if details:
            add_line = True
            sms += f'💼 {details[0]}'
            for t in details[1:]:
                sms += f' / {t}'

            sms += '\n'

        if add_line:
            sms += '\n'

        sms += job.body
