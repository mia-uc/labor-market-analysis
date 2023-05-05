from src.etl_process.python_mongo_tools import MongoInterfaces
from src.etl_process.jobs_db_center import JobsDBCenter


class LaborumTransformer:
    def __init__(self, job) -> None:
        self.job = job

        try:
            company = self.job['aviso']['empresa']
            self.city = company['ciudad']
        except:
            self.city = None

    def __getattr__(self, __name: str):

        try:
            return self.job[__name]
        except KeyError:
            return None

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
    def published_at(self):
        return self.job['fechaPublicacion']

    @property
    def body(self):
        return self.job['detalle']


class LaborumCleanPipeline:
    def __init__(self, force=False) -> None:
        self.db = MongoInterfaces('Laborum')
        self.force = force

    def filtered_data(self):
        aggregate = []

        _match = {
            'aviso': {  # If body is defined meats the job was fully scrapped
                '$exists': True
            },
            'aviso.area.stringId': {  # It only matter if is a jobs of IT
                # Comercial, Ventas y Negocios
                # Oficios y Otros
                # Administración, Contabilidad y Finanzas
                # Abastecimiento y Logística
                # Atención al Cliente, Call Center y Telemarketing
                # Producción y Manufactura
                # Gastronomía y Turismo
                # Salud, Medicina y Farmacia
                # Recursos Humanos y Capacitación
                # Ingenierías
                # Minería, Petróleo y Gas
                # Educación, Docencia e Investigación
                # Seguros
                # Tecnología, Sistemas y Telecomunicaciones
                # Marketing y Publicidad
                # Ingeniería Civil y Construcción
                # Secretarias y Recepción
                # Legales
                # Diseño
                # Comunicación, Relaciones Institucionales y Públicas
                # Aduana y Comercio Exterior
                # Gerencia y Dirección General
                # Sociología / Trabajo Social
                # Departamento Tecnico
                # Enfermería

                '$in': [
                    'tecnologia-sistemas-y-telecomunicaciones'
                ]
            }
        }

        if not self.force:
            # Take only the data witch have synced yet
            _match['already_fetch'] = {'$exists': False}

        aggregate.append({'$match': _match})
        return self.db.doc.aggregate(aggregate)

    def run(self, centered_db: JobsDBCenter):

        for job in self.filtered_data():
            self.migrate(job, centered_db)

    def migrate(self, job, centered_db, **info):
        transformed_job = LaborumTransformer(job)
        centered_db.migrate(
            _id=transformed_job.id,
            name=transformed_job.titulo,
            min_salary=transformed_job.salarioMinimo,
            max_salary=transformed_job.salarioMinimo,
            seniority=transformed_job.seniority,
            work_modality=transformed_job.modality,
            contract_type=transformed_job.contract,
            published_at=transformed_job.published_at,
            hiring_organization=transformed_job.empresa,
            description=transformed_job.body,
            country='Chile',
            city=transformed_job.city,
            origin='Laborum',
            currency='clp',
            **info,
        )

        print(
            f"..... Cleaning the job => {transformed_job.id} => {transformed_job.titulo}"
        )

        self.db.update({'already_fetch': True}, **{'id': job['id']})
