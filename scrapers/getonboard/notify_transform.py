from transformers import Transformer


class GetOnBoardNotifyTransformer(Transformer):

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

    @property
    def currency(self):
        return 'usd'

    @property
    def origin(self):
        return 'GetOnBoard'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.title,
            'min_salary': self.min_salary,
            'max_salary': self.max_salary,
            'experience': self.seniority,
            'work_modality': self.modality,
            'contract_type': self.contract,
            'published_at': self.published_at,
            'hiring_organization': self.hiring_organization,
            'description': self.body,
            'country': self.country,
            'city': self.city,
            'origin': 'GetOnBoard',
            'currency': 'usd',
        }
