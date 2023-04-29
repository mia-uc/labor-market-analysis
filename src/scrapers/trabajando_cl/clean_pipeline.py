from src.etl_process.python_mongo_tools import MongoInterfaces
from src.etl_process.jobs_db_center import JobsDBCenter
from bs4 import BeautifulSoup


class WorkingCLTransformer:
    def __init__(self, job) -> None:
        self.job = job

    def __getattr__(self, __name: str):

        try:
            return self.job[__name]
        except KeyError:
            return None
        

    @property
    def contract(self):
        # 'Free Lance', 'Comisionista',
        # 'Jornada Completa', 'En terreno', 
        # 'Mixta (Teletrabajo + Presencial)', 
        # 'Part Time', 'Por Turnos', 'Práctica', 
        # 'Teletrabajo', 'Reemplazo'

        try:
            contract = self.job['nombreJornada'] 
 
            if contract == 'Part Time':
                return 'part-time'
            if contract == 'Free Lance':
                return 'freelance'
            if contract == 'Práctica':
                return 'internship'
            if contract == 'Por Turnos':
                return 'in-turns'

            return 'full-time'
        except KeyError:
            pass
        
        return None

    @property
    def modality(self):

        # 'Free Lance', 'Comisionista',
        # 'Jornada Completa', 'En terreno', 
        # 'Mixta (Teletrabajo + Presencial)', 
        # 'Part Time', 'Por Turnos', 'Práctica', 
        # 'Teletrabajo', 'Reemplazo'

        try:
            modality = self.job['nombreJornada'] 

            if modality == 'Mixta (Teletrabajo + Presencial)':
                return 'hybrid'    
            if modality in ['Teletrabajo', 'Free Lance']:
                return 'remote'

            return 'on-place'
        except KeyError:
            return None
        
    @property
    def seniority(self):
        try:
            verb =  self.job['nombreOperadorExperiencia']

            if verb == 'Sin experiencia':
                return 'without-experience'

        except:
            pass

        try:
            experiences =  self.job['aniosExperiencia']

            if experiences > 3:
                return 'senior'

            if experiences > 1:
                return 'semi-senior'
            
            return 'junior'
        except:
            pass

        return None
    
    @property
    def published_at(self):
        return self.job['fechaExpiracionFormatoIngles']

    @property
    def hiring_organization(self):
        try:
            return self.job['nombreEmpresaFigurar']
        except:
            pass

        try:
            return self.job['nombreEmpresaFantasia']
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

            raise Exception(currency)
        except KeyError:
            return None

class WorkingCLCleanPipeline:
    def __init__(self, force = False) -> None:
        self.db = MongoInterfaces('Trabajando.cl')
        self.force = force

    def filtered_data(self):
        aggregate = []

        _match = {
            'nombreArea': { # If body is defined meats the job was fully scrapped
                '$exists': True,
                '$in': [
                    "Desarrollo de Producto",
                    "Proyectos", 
                    "Computación e Informática", 
                    "Planificación y Desarrollo", 
                    "Informática","Desarrollo"
                    "Inteligencia de Negocios", 
                    "Investigación",
                    "Tecnologías de Información", 
                    "Informática - hardware", 
                    "Investigación de mercados"
                ]
            },
            # "Educación / Docencia", "Construcción", "Finanzas", "Desarrollo de Producto", "Derecho Mercantil", 
            # "Proyectos", "Comercial", "Computación e Informática", "Planificación y Desarrollo"
            # "Servicios Generales", "Decoración", "Banca y Servicios Financieros", "Agronomía", "Seguros", "Recepción"
            # "Servicio Técnico", "Mecánica", "Envasado", "Salud", "Prevención de Riesgos", "Contabilidad", "Estética", "Medicina y Salud"
            # "Capacitación", "Calidad", "Alimentos y Bebidas", "Química", "Reclutamiento y Selección", "Estimulación temprana", "Arquitectura", "Derecho", 
            # "Distribución", "Operaciones", "Marketing / Mercadeo", "Aseo", "Cobranza", "Control de Gestión", "Propiedades"
            # "Informática", "Servicios Sociales", "Nóminas", "Administración", "Tributarios", "Ventas"
            # "Desarrollo", "Comunicación / Medios", "Recursos Humanos", "Facturación", "Diseño de Confecciones", "Publicidad", "Inteligencia de Negocios"
            # "Producción y Manufactura", "Dibujante", "Servicios de Seguridad", "Investigación", "Electricidad", "Post Venta", "Medio Ambiente"
            # "Secretaria Bilingue", "Cuentas clave", "Ambiental", "Turismo y Hotelería", "Tecnologías de Información", "Servicio al Cliente"
            # "Seguridad e Higiene", "Industria", "Administración Pública", "Informática – hardware", "Soporte Administrativo", "Auditoría"
            # "Call Center", "Laboratorio", "Compras", "Gastronomía", "Mantención", "Despacho", "Logística"
            # "Otra Área", "Investigación de mercados", "Asistente y Secretaria", "Diseño", "Ingeniería", "Clinica"
            # "Relaciones Públicas", "Abastecimiento", "Servicios", "Silvicultura en bosque"

        }

        if not self.force:
            # Take only the data witch have synced yet
            _match['already_fetch'] = {'$exists': False}

        aggregate.append({'$match': _match})
        return self.db.doc.aggregate(aggregate)
    
    def run(self, centered_db: JobsDBCenter):

        for i, job in enumerate(self.filtered_data()):
            transformed_job = WorkingCLTransformer(job)

            centered_db.migrate(
                _id = transformed_job.idOferta,
                name = transformed_job.cargo,
                min_salary = transformed_job.salary,
                max_salary = transformed_job.salary,
                seniority = transformed_job.seniority,
                work_modality = transformed_job.modality,
                contract_type = transformed_job.contract,
                published_at = transformed_job.published_at,
                hiring_organization = transformed_job.hiring_organization,
                description = transformed_job.body,
                country = transformed_job.country,
                city = transformed_job.city,
                origin = 'Trabajando.cl',
                currency = transformed_job.currency
            )

            print(f"..... Cleaning the job #{i} => {transformed_job.idOferta} => {transformed_job.cargo}")

            self.db.update({'already_fetch': True}, **{'id': transformed_job.idOferta})
    



