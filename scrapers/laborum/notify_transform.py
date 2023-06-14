from transformers import Transformer


class LaborumNotifyTransformer(Transformer):

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
    def body(self):
        return self.job['detalle']

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.titulo,
            'min_salary': self.salarioMinimo,
            'max_salary': self.salarioMaximo,
            'experience': self.seniority,
            'work_modality': self.modality,
            'contract_type': self.contract,
            'published_at': self.published_at,
            'hiring_organization': self.empresa,
            'description': self.body,
            'country': 'Chile',
            'city': self.city,
            'origin': 'Laborum',
            'currency': 'clp',
        }
