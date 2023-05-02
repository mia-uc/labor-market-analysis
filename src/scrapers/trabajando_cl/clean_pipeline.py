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
            '$or': [
                {
                    'nombreArea': { # If body is defined meats the job was fully scrapped
                        '$exists': True,
                        '$in': [
                            "Desarrollo de Producto",
                            "Proyectos", 
                            "Computación e Informática", 
                            "Planificación y Desarrollo", 
                            "Informática",
                            "Desarrollo",
                            "Inteligencia de Negocios", 
                            "Investigación",
                            "Tecnologías de Información", 
                            "Informática - hardware", 
                            "Investigación de mercados"
                        ]
                    },
                },
                {
                    "carreras": {
                        "$exists": True, 
                        "$ne": [],
                        "$elemMatch": {
                            "nombreCarrera": {
                            "$in":  [
                                "Técnico en Computación e Informática", 
                                "Técnico en Soporte Computacional",
                                "Diseño y Programación Multimedia / Diseño Digital", 
                                "Ingeniería en Bioinformática", 
                                "Ingeniería en Gestión e Informática", 
                                "Licenciatura en Computación", 
                                "Ingeniería Ejecución Web Manager", 
                                "Ingeniería de Sistemas de Información Empresarial y Control de Gestión",
                                "Ingeniería en Automatización y Robótica", 
                                "Técnico de Nivel Superior en Computación", 
                                "Tecnologías De La Información y Comunicación", 
                                "Ingeniería en Computación e Informática", 
                                "Ingeniería en Estadística", 
                                "Técnico Universitario en Telecomunicaciones y Redes",
                                "Informática", "Ingeniería en Informática / Sistemas", 
                                "Ingeniería en Conectividad y Redes", 
                                "Análisis de Sistemas / Analista Programador", 
                                "Ingeniería en Computación", 
                                "Ingeniería en Telemática", 
                                "Ingeniería Civil en Computación e Informática", 
                                "Programación", 
                                "Ingeniería Computación Informática y Comunicaciones",
                            ] 
                           }
                         }
                    }
                }
             ]
        }

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


# "Técnico en Computación e Informática", "Técnico en Soporte Computacional",
# "Diseño y Programación Multimedia / Diseño Digital", "Ingeniería en Bioinformática", "Ingeniería en Gestión e Informática",
# "Licenciatura en Computación", "Ingeniería Ejecución Web Manager", "Ingeniería de Sistemas de Información Empresarial y Control de Gestión",
# "Ingeniería en Automatización y Robótica", "Técnico de Nivel Superior en Computación", "Tecnologías De La Información y Comunicación",
# "Ingeniería en Computación e Informática", "Ingeniería en Estadística", "Técnico Universitario en Telecomunicaciones y Redes",
# "Informática", "Ingeniería en Informática / Sistemas", "Ingeniería en Conectividad y Redes", "Análisis de Sistemas / Analista Programador",
# "Ingeniería en Computación", "Ingeniería en Telemática", "Ingeniería Civil en Computación e Informática",
# "Programación", "Ingeniería Computación Informática y Comunicaciones",


# "Pedagogía en Música / Arte"
# "Técnico en Restauración"
# "Arquitectura"
# "Química De Materiales"
# "Laboratorista Químico Minero"
# "Técnico en Fabricación y montaje Industrial"
# "Derecho"
# "Bar Training"
# "Técnico Superior en administración cooperativa y mutual"
# "Tecnólogo / Técnico en Construcción"
# "Técnico en Metalmecánica"
# "Ingeniería en Logística"
# "Ingeniería Electrónica"
# "Técnico en Masoterapia"
# "Ingeniería en Maquinaria y Vehículos Automotrices"
# "Biología Marina"
# "Música  "
# "Técnico Asistente del Educador de Párvulos"
# "TÉCNICO EN GEOLOGÍA"
# "Kinesiología"
# "Nutrición y Dietética"
# "PEDAGOGÍA EN HISTORIA, GEOGRAFÍA Y CIENCIAS SOCIALES"
# "Ingeniería en Administración de Empresas"
# "Técnico en Administración de Recursos Humanos y Personal"
# "Licenciatura en Física"
# "Técnico en Diseño editorial"
# "Ingeniería en Administración Industrial"
# "Enseñanza Media o Superior"
# "Ingeniería Pesquera / Cultivos Marinos"
# "Dirección de Arte"
# "Ingeniería en Administración de Operaciones"
# "Ingeniería en Control e Instrumentación Industrial"
# "Ingeniería en Minas y Metalúrgia"
# "Técnico Superior en Administración Agrícola"
# "Ingeniería en Recursos Naturales Renovables"
# "Manteniemiento de Maquinaria Pesada"
# "Producción Gastronómica"
# "Pedagogía en Filosofía"
# "Licenciatura en Artes Visuales"
# "Dirección y Producción"
# "Tecnología Industrial de los alimentos"
# "Pedagogía Educación Media en Lenguaje y Comunicación"
# "Biología"
# "Técnico en Computación e Informática"
# "Técnico agente o visitador médico"
# "Técnico en alimentos"
# "Publicidad Profesional Mención Marketing y Medios"
# "Técnico de Nivel Superior en Administración de Negocios Gastronómicos"
# "Técnico en Soporte Computacional"
# "Diseño y Programación Multimedia / Diseño Digital"
# "Frigorista Electromecánico"
# "Ingeniería en Administración Hotelera Internacional"
# "Ingeniería de Ejecución en Administración"
# "Pedagogía en Idiomas"
# "Ingeniería en Bioinformática"
# "Ingeniería en Sonido"
# "Técnico en Administración de Programas Sociales"
# "Ingeniería Ejecución Administración de Empresas"
# "Ingeniería en Turismo y Hotelería"
# "Ingeniería en Gestión e Informática"
# "Licenciatura en Computación"
# "Pedagogía en Ciencias "
# "Técnico en acuicultura y pesca"
# "Ingeniería Civil en Obras Civiles"
# "Gastronomía / Cocina"
# "Odontología"
# "Negocios Internacionales"
# "Pedagogía en Lengua Castellana y Comunicación"
# "Técnico Jurídico"
# "Dibujo Industrial"
# "Ingeniería en Deportes"
# "Licenciatura en Producción de Bio-Imágenes"
# "Tecnología Industrial de alimentos del mar"
# "Publicidad Técnica Mención Marketing Promocional"
# "Técnico en Mecánica Automotriz"
# "Bíoanalisis / Biotecnología Industrial"
# "Ingeniería en Control de Gestión"
# "Técnico en óptica"
# "Arqueología"
# "Ingeniería en Gestión de Negocios"
# "Ingeniería en Gestión de Calidad y Ambiente"
# "Técnico en Diseño de Espacios y Equipamientos"
# "Ingeniería en Gestión y Control de Calidad"
# "Administración de Predios Agrícolas"
# "Teología"
# "Ingeniería en Telecomunicaciones
# "Ingeniería en Alimentos"
# "Técnico en terapias naturales y naturopatía"
# "Ingeniería en Gestión"
# "Psicopedagogía"
# "Matemática "
# "Administración de Empresas Turísticas"
# "Geomensura / Topografía / Agrimensura"
# "Psicología Laboral"
# "Psicología"
# "Diseño de Interiores y Mobiliario"
# "MBA"
# "Ingeniería Hidráulica"
# "Licenciatura en Seguridad e Higiene en el Trabajo"
# "Ingeniería en Climatización"
# "Ingeniería Ejecución Web Manager"
# "Técnico Productor en Medios Visuales"
# "Ingeniería de Sistemas de Información Empresarial y Control de Gestión"
# "Doctorado"
# "Economía "
# "Pedagogía Media / Educación Media / Secundaria"
# "Diseño Editorial"
# "Ingeniería en Automatización y Robótica"
# "Licenciatura en Literatura / Literatura / Letras"
# "Higienista Dental"
# "Diplomado"
# "Técnico de Nivel Sup. en Guía Turístico en la Naturaleza"
# "Técnico en Mecánica Industrial"
# "Pedagogía en Matemáticas / Computación"
# "Ingeniería en Gestión Turística"
# "Bioquímica"
# "Ingeniería Civil Química"
# "Técnico de Nivel Superior en Computación"
# "Técnico en control de calidad"
# "Técnico en Laboratorio Clínico"
# "Técnico en Comercio Exterior"
# "Turismo de Aventura"
# "Ingeniería en Mecatrónica"
# "Cine / Séptimo Arte"
# "Bachillerato en Arte"
# "Pedagogía en Educación Física y Deporte"
# "Técnico en Instrumentación,Automatización y Control Industrial"
# "Tecnologías De La Información y Comunicación"
# "Ingeniería civil en minas"
# "Diseño y Producción de Areas Verdes"
# "Técnico en Electrónica y Electrónica Industrial"
# "Laboratorio Dental / Mecánica Dental"
# "Ingeniería en Agronomía"
# "Administración Pública"
# "Terapia Física"
# "Técnico en procesos industriales"
# "Estadísticas"
# "Técnico en Planificación Vial"
# "Mecánica"
# "Ingeniería en Transporte"
# "Diseño Digital"
# "Licenciatura en Ciencias Biológicas"
# "Periodismo"
# "Diseño"
# "Ingeniería civil ambiental"
# "Técnico en Instrumentación, Automatización y Control Industrial"
# "Actuación y Teatro"
# "Artes Visuales"
# "Ingeniería en Computación e Informática"
# "Técnico de Nivel Superior en Actividad Física y Deportes"
# "Fisioterapia"
# "Técnico en Climatización"
# "Ingeniería en Recursos Humanos"
# "Magister"
# "Ingeniería"
# "Licenciatura en Recursos Humanos"
# "Técnico en Minería y Metalúrgica"
# "Ingeniería en Marina Mercante"
# "Prevención de Riesgos / Seguridad Industrial "
# "Tecnología en Metalurgia"
# "Cosmetología"
# "Animación Digital"
# "Ingeniería de Diseño / Automatización Electrónica"
# "Pedagogía en Educación Diferencial"
# "Fonoaudiología"
# "Licenciatura en Química"
# "Psicología Clínica"
# "Hotelería / Administración Hotelera"
# "ADMINISTRACIÓN TURÍSTICA Y HOTELERA"
# "Ingeniería de Ejecución en Administración Hotelera"
# "Administración en Alimentación Colectiva"
# "Química y Farmacia"
# "Tecnología Médica"
# "Técnico en Mantención"
# "Construcción Civil"
# "Administración y Evaluación De Proyectos"
# "Administración de Ventas"
# "Finanzas Bancarias / Negocios Internacionales"
# "Técnico en Podología"
# "Asistente Social"
# "Ingeniería en Ejecución Mecánica"
# "Técnico en Enfermería"
# "Paisajismo / Diseño de Paisaje  "
# "Licenciatura en Matemática"
# "Contador Público y Auditor"
# "Técnico en Edificación"
# "Administración Empresas en Marketing y Comunicación Digital"
# "Ingeniería en Ordenación Ambiental"
# "Filosofía"
# "Administración de Negocios Internacionales"
# "Bibliotecología / Documentación"
# "Técnico en Comunicación Audiovisual"
# "Secretariado Bilingue"
# "Comunicación Audiovisual y/o Multimedia"
# "Ingenieria Civil en Sonido"
# "Técnico en Contabilidad General"
# "Químico Laboratista Industrial"
# "Matrón (a)"
# "Técnico / Tecnólogo / Técnico Superior"
# "Electromecánico"
# "Control de Gestión"
# "Ingeniería Industrial"
# "Técnico en Logística"
# "Pedagogía en Biología y Ciencias Naturales"
# "Técnico en Matricería"
# "Mecatrónica"
# "Ingeniería Ejecución en Gestión Industrial"
# "Fotografía"
# "Ingeniería de Petróleos / Petroquímica"
# "Psicología Educacional"
# "Técnico en Mecánica"
# "Técnico en Administración de Empresas"
# "Medicina Veterinaria"
# "Administración Hotelera Profesional"
# "Ingeniería en Refrigeración y Climatización"
# "Ingeniero Naval"
# "Pedagogía en Educación Básica"
# "Informática Biomédica"
# "Técnico de Nivel Superior en Organización y Producción de Eventos"
# "Ingeniería en Estadística"
# "Asistente Ejecutivo"
# "Periodismo Deportivo"
# "Contactología"
# "Ingeniería en Acuicultura y Pesca"
# "Antropología"
# "Creación e Interpretación Musical"
# "Geoquímica"
# "Licenciatura en Arte / Bellas Artes"
# "Técnico en Turismo y Hotelería"
# "Orientación Familiar"
# "Técnico en Prevención de Riesgos"
# "Administración gastronómica"
# "Ingeniería en Gestión y Desarrollo Tecnológico"
# "Ingeniería Civil en Energías Renovables"
# "Ingeniería en Recursos Naturales"
# "Técnico en Medio Ambiente"
# "Pedagogía en Religión"
# "Técnico en Sonido"
# "Sociología"
# "Técnico en Oleohidráulica y Neumática"
# "Administración de Empresas e Ing. Asociadas"
# "Medicina "
# "Técnico en Construcción y Obras Civiles"
# "Técnico Universitario en Telecomunicaciones y Redes"
# "Actuario"
# "Técnico en Administración de Redes y Soporte"
# "Otra carrera"
# "Electrónica"
# "Técnico Marino"
# "Técnico en Refrigeración"
# "Ciencias Políticas"
# "Técnico Financiero"
# "Pedagogía en Cs. Naturales y Química"
# "Turismo Técnico Mención Tráfico y Carga Aérea"
# "Bachiller en Ciencias Religiosas"
# "Ingenieria en Biotecnología"
# "Bachillerato en Ciencias"
# "Relaciones del Trabajo"
# "Ingeniería Geomática"
# "Ingeniería en Geomensura"
# "Técnico en Economía y Administración de la pequeñas y mediana empresa"
# "Ingeniería en Construcción"
# "Ilustración Digital"
# "Técnico en Diseño Gráfico"
# "Ingeniería Forestal"
# "Licenciatura en Ciencias Religiosas y Estudios Eclesiásticos"
# "Secretariado"
# "Ingeniería Civil en Electricidad"
# "Administración de Empresas de Servicios"
# "Cartografía"
# "Tecnología y Administración Agrícola"
# "Tecnología Pecuaria"
# "Ingeniería en Metalmecánica"
# "Ingeniería en Medio Ambiente"
# "Construcciones Metálicas"
# "TÉCNICO EN TRANSPORTE MARÍTIMO Y PUERTOS"
# "Ingeniería en Automatización y Control Industrial"
# "Técnico en Química (Análisis e Industrial)"
# "Ingenieria en RRHH"
# "Ingeniería de Ejecución en Administración Turística"
# "Doctorado Ciencias de la Educación"
# "Ingeniería Civil Eléctrica"
# "Administración De Autotransporte y Logística"
# "Informática"
# "Ingeniería en Informática / Sistemas"
# "Ingeniería en Conectividad y Redes"
# "Clasificación Arancelaria y Despacho Aduanero"
# "Artes / Artes Plásticas / Artes Gráficas"
# "Auxiliar Paramédico"
# "Técnico de Nivel Superior en Vitivinicultura y Enología"
# "Terapia Ocupacional"
# "Ingeniería en Proyectos Industriales"
# "Ingeniería en manufactura industrial"
# "Danza / Interpretación en Danza "
# "Ingeniería en Geografía"
# "Turismo Técnico Mención Empresas de Viajes"
# "Administración y Producción Agropecuaria"
# "Ingeniería en Prevención de Riesgos"
# "Ingeniería de Ejecución Industrial"
# "Traducción e Interpretación"
# "Análisis de Sistemas / Analista Programador"
# "Socioeconomía"
# "Técnico en Trabajo Social"
# "Pedagogía en Cs. Naturales y Física"
# "Dirección y Producción de eventos"
# "Administración Financiera"
# "Mantenimiento de Maquinaria de Planta"
# "Pedagogía Media en Religión y Educación Moral"
# "Comercialización"
# "Biotecnología / Bioingeniería"
# "Ingeniería en Computación"
# "Ingeniería Agropecuaria"
# "Geominería"
# "Trabajo Social"
# "Técnico asistente del educador diferencial"
# "Pastelería Internacional"
# "Técnico en geominería"
# "Ingeniería en Administración Agroindustrial"
# "Pedagogía en Lenguaje y Literatura"
# "Historia del Arte"
# "Ingeniería Civil Electrónica"
# "Ingeniería Diseño de Productos"
# "Educación Física"
# "Recursos Humanos / Relaciones Industriales"
# "Técnico en Farmacia"
# "Ingeniería en Información y Control de Gestión"
# "Administración de Hoteles y Restaurantes"
# "Ingeniería en Agronegocios"
# "Técnico agropecuario"
# "Técnico en Arte y Gestión Cultural"
# "Nutrición y Alimentación Institucional"
# "Técnico en Tránsito y Transporte"
# "Ingeniería Mecánica"
# "Venta y Publicidad"
# "Administración Industrial"
# "Procesos Agroindustriales"
# "Técnico en peluquería y estética"
# "Asistente Judicial"
# "Ingeniería en Marketing"
# "Licenciatura en Educación / Magisterio"
# "Ingeniería en Bioprocesos
# "Técnico en Electricidad y Electricidad Industrial"
# "Ingeniería Civil en Minas"
# "Ingeniería en Telemática"
# "Diseño y Producción Industrial"
# "Licenciatura en Ciencias del Medio Ambiente"
# "Relaciones Públicas"
# "Técnico Veterinario"
# "Ingeniería Agrícola"
# "Técnico en Topografia"
# "Ingeniería en Mantenimiento Industrial"
# "Obstetricia y Puericultura"
# "Ingeniería en transporte marítimo"
# "Técnico Dental y Asistente de Odontología"
# "Contador Auditor"
# "Ingeniería en Ejecución Electrónica"
# "Ingeniería en Construcción Civil"
# "Ingeniería Civil en Computación e Informática"
# "Técnico en Servicio Social"
# "Publicidad"
# "Ingeniería Mecánica en Producción Industrial"
# "Comunicación Social / Empresarial"
# "Ingeniería Civil en Agroindustrias"
# "Preparador Físico"
# "Administración Gastronómica Internacional"
# "Química Industrial"
# "Técnico de Radiología y Radioterapia"
# "Ingeniería de Ejecución en Mecánica Automotriz y Autotrónica"
# "Ingeniería en Física"
# "Sistemas de Gestión de la Calidad"
# "Ingeniería Civil Metalúrgica"
# "Programación"
# "Administrador Universitario de Empresas"
# "Ciencias Físicas"
# "Técnico en Electricidad Industrial"
# "Técnico en Salud Natural y Terapias Complementarias"
# "Microbiología industrial de alimentos"
# "Marketing"
# "Ingeniería Civil Industrial"
# "Paramédico"
# "Astronomía"
# "Conservación Industrial de Alimentos por Frío"
# "Tecnología en Minería y Metalurgía"
# "Tecnólogo / Técnico Control Industrial"
# "Ingenieria en Comercio / Negocio Internacional"
# "Ingeniería Matemáticas"
# "Técnico en Comunicación para las Organizaciones Sociales"
# "Tecnología y Administración Pecuaria"
# "Ingeniería en Ejecución Eléctrica"
# "Ingeniería Civil"
# "Química"
# "Técnico en Deporte, Recreación y Preparación Física"
# "Dibujo y Proyectos Industriales"
# "Diseño de Vestuario"
# "Biología en Gestión de Recursos Naturales"
# "Ingeniería de Producción"
# "Física / Ciencias Físicas"
# "Ingeniería Comercial"
# "Ingeniería en Aviación Comercial"
# "Ingeniería Aerospacial / Aeronáutica"
# "Agronomía"
# "Electrónica de Sistemas Computarizados"
# "Diseño Gráfico"
# "Maestría en Dirección Comercial"
# "Ingeniería Biomédica"
# "Producción Musical"
# "Pedagogía en Español"
# "Ingeniería Civil Mecánica"
# "Técnico Profesional Archivero"
# "Técnico en Gestión y Control de calidad"
# "Técnico de Nivel Superior en Bioprocesos Industriales"
# "Diseño Industrial"
# "Diseño de Objetos y Ambientes"
# "Técnico en Mantenimiento Industrial"
# "Magister en Ciencias de la Educación"
# "Técnico en traducción e interpretariado"
# "Ingeniería Química"
# "Diseño de Interiores / Decoración"
# "Dibujo de Proyectos de Arquitectura e Ingenieria"
# "Dibujo Técnico"
# "Técnico en Geomensura"
# "Ingeniería Computación Informática y Comunicaciones"
# "Ingeniería Bioquímica"
# "Geografía"
# "Licenciatura en Filosofía"
# "Ingeniería en Electricidad"
# "Pedagogía"
# "Pedagogía en Educación de Párvulos"
# "Ingeniería Civil Matemática"
# "Administración de Procesos Productivos"
# "Técnico En Bienestar Social"
# "Administración Hotelera Internacional"
# "Enfermería"
# "Servicios  Posventa Área Automotriz"

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
    



