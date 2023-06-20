from transformers import Transformer
from bs4 import BeautifulSoup


class WorkingCLNotifyTransformer(Transformer):

    @property
    def name(self):
        if 'cargo' in self.job:
            return self.job['cargo']
        if 'nombreCargo' in self.job:
            return self.job['nombreCargo']

        raise Exception(f"No se detector el nombre el job {self.idOferta}")

    @property
    def contract(self):
        # 'Full-time',
        # 'Part-time',
        # 'Por Horas',
        # 'Temporario',
        # 'Por Contrato',
        # 'Fines de Semana',
        # 'Nocturno',
        # 'Pasantia

        try:
            if self.job['tipoTrabajo'] == 'Full-time':
                return 'full-time'
            if self.job['tipoTrabajo'] == 'Part-time':
                return 'part-time'
            if self.job['tipoTrabajo'] == 'Por Contrato':
                return 'freelance'
            if self.job['tipoTrabajo'] == 'Pasantia':
                return 'internship'
            if self.job['tipoTrabajo'] == 'Por Horas':
                return 'per-hours'
            if self.job['tipoTrabajo'] == 'Fines de Semana':
                return 'weekends'
            if self.job['tipoTrabajo'] == 'Nocturno':
                return 'at-night'

        except KeyError:
            pass

        return None

    @property
    def modality(self):
        # 'fully_remote', 'hybrid', 'remote_local', 'no_remote', 'temporarily_remote'
        try:
            if self.job['modalidadTrabajo'] == 'Presencial':
                return 'on-place'
            if self.job['modalidadTrabajo'] == 'Híbrido':
                return 'hybrid'
            if self.job['remote_modality'] == 'Remoto':
                return 'remote'

            return 'hybrid'
        except KeyError:
            return None

    @property
    def seniority(self):
        # 'Senior', 'Junior', 'Senior / Semi-Senior',
        # 'Semi Sr', 'Otro',
        # 'Jefe / Supervisor / Responsable',
        # 'Trainee / Pasante',
        # 'Sin Experiencia',
        # 'Gerencia / Alta Gerencia / Dirección

        try:
            experiences = self.job['aviso']['nivelLaboral']['nombre']

            if experiences in ['Senior', 'Senior / Semi-Senior']:
                return 'senior'

            if experiences == 'Semi Sr':
                return 'semi-senior'

            if experiences in ['Junior', 'Trainee / Pasante']:
                return 'junior'

            if experiences == 'Sin Experiencia':
                return 'without-experience'

        except:
            pass

        return None

    @property
    def body(self):
        soup = BeautifulSoup(self.job['descripcionOferta'], "html.parser")
        text = soup.get_text()

        try:
            soup = BeautifulSoup(self.job['requisitosMinimos'], "html.parser")
            requirement = soup.get_text()
        except:
            return text

        return f'{text}\n\n{requirement}'

    @property
    def salary(self):
        try:
            value = self.job['sueldo']
            if value > 0:
                return value
        except:
            pass

        return None

    @property
    def city(self):
        try:
            return self.job['ubicacion']['nombreRegion']
        except:
            return None

    @property
    def country(self):
        try:
            return self.job['ubicacion']['nombrePais']
        except:
            return None

    @property
    def currency(self):
        try:
            currency = self.job['nombreMoneda']

            if currency == 'Dólares':
                return 'usd'

            if currency == 'Pesos Chilenos':
                return 'clp'

            if currency:
                raise Exception(currency)
        except KeyError:
            return None

    def to_dict(self):
        return {
            "id": self.idOferta,
            "name": self.name,
            'min_salary': self.salary,
            'max_salary': self.salary,
            'experience': self.seniority,
            'work_modality': self.modality,
            'contract_type': self.contract,
            'published_at': self.published_at,
            'hiring_organization': self.hiring_organization,
            'description': self.body,
            'country': self.country,
            'city': self.city,
            'origin': 'Trabajando.cl',
            'currency': self.currency,
        }
