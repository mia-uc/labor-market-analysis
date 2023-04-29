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






# 0
# "Pedagogía en Música / Arte"
# 1
# "Técnico en Restauración"
# 2
# "Arquitectura"
# 3
# "Química De Materiales"
# 4
# "Laboratorista Químico Minero"
# 5
# "Técnico en Fabricación y montaje Industrial"
# 6
# "Derecho"
# 7
# "Bar Training"
# 8
# "Técnico Superior en administración cooperativa y mutual"
# 9
# "Tecnólogo / Técnico en Construcción"
# 10
# "Técnico en Metalmecánica"
# 11
# "Ingeniería en Logística"
# 12
# "Ingeniería Electrónica"
# 13
# "Técnico en Masoterapia"
# 14
# "Ingeniería en Maquinaria y Vehículos Automotrices"
# 15
# "Biología Marina"
# 16
# "Música  "
# 17
# "Técnico Asistente del Educador de Párvulos"
# 18
# "TÉCNICO EN GEOLOGÍA"
# 19
# "Kinesiología"
# 20
# "Nutrición y Dietética"
# 21
# "PEDAGOGÍA EN HISTORIA, GEOGRAFÍA Y CIENCIAS SOCIALES"
# 22
# "Ingeniería en Administración de Empresas"
# 23
# "Técnico en Administración de Recursos Humanos y Personal"
# 24
# "Licenciatura en Física"
# 25
# "Técnico en Diseño editorial"
# 26
# "Ingeniería en Administración Industrial"
# 27
# "Enseñanza Media o Superior"
# 28
# "Ingeniería Pesquera / Cultivos Marinos"
# 29
# "Dirección de Arte"
# 30
# "Ingeniería en Administración de Operaciones"
# 31
# "Ingeniería en Control e Instrumentación Industrial"
# 32
# "Ingeniería en Minas y Metalúrgia"
# 33
# "Técnico Superior en Administración Agrícola"
# 34
# "Ingeniería en Recursos Naturales Renovables"
# 35
# "Manteniemiento de Maquinaria Pesada"
# 36
# "Producción Gastronómica"
# 37
# "Pedagogía en Filosofía"
# 38
# "Licenciatura en Artes Visuales"
# 39
# "Dirección y Producción"
# 40
# "Tecnología Industrial de los alimentos"
# 41
# "Pedagogía Educación Media en Lenguaje y Comunicación"
# 42
# "Biología"
# 43
# "Técnico en Computación e Informática"
# 44
# "Técnico agente o visitador médico"
# 45
# "Técnico en alimentos"
# 46
# "Publicidad Profesional Mención Marketing y Medios"
# 47
# "Técnico de Nivel Superior en Administración de Negocios Gastronómicos"
# 48
# "Técnico en Soporte Computacional"
# 49
# "Diseño y Programación Multimedia / Diseño Digital"
# 50
# "Frigorista Electromecánico"
# 51
# "Ingeniería en Administración Hotelera Internacional"
# 52
# "Ingeniería de Ejecución en Administración"
# 53
# "Pedagogía en Idiomas"
# 54
# "Ingeniería en Bioinformática"
# 55
# "Ingeniería en Sonido"
# 56
# "Técnico en Administración de Programas Sociales"
# 57
# "Ingeniería Ejecución Administración de Empresas"
# 58
# "Ingeniería en Turismo y Hotelería"
# 59
# "Ingeniería en Gestión e Informática"
# 60
# "Licenciatura en Computación"
# 61
# "Pedagogía en Ciencias "
# 62
# "Técnico en acuicultura y pesca"
# 63
# "Ingeniería Civil en Obras Civiles"
# 64
# "Gastronomía / Cocina"
# 65
# "Odontología"
# 66
# "Negocios Internacionales"
# 67
# "Pedagogía en Lengua Castellana y Comunicación"
# 68
# "Técnico Jurídico"
# 69
# "Dibujo Industrial"
# 70
# "Ingeniería en Deportes"
# 71
# "Licenciatura en Producción de Bio-Imágenes"
# 72
# "Tecnología Industrial de alimentos del mar"
# 73
# "Publicidad Técnica Mención Marketing Promocional"
# 74
# "Técnico en Mecánica Automotriz"
# 75
# "Bíoanalisis / Biotecnología Industrial"
# 76
# "Ingeniería en Control de Gestión"
# 77
# "Técnico en óptica"
# 78
# "Arqueología"
# 79
# "Ingeniería en Gestión de Negocios"
# 80
# "Ingeniería en Gestión de Calidad y Ambiente"
# 81
# "Técnico en Diseño de Espacios y Equipamientos"
# 82
# "Ingeniería en Gestión y Control de Calidad"
# 83
# "Administración de Predios Agrícolas"
# 84
# "Teología"
# 85
# "Ingeniería en Telecomunicaciones"
# 86
# "Ingeniería en Alimentos"
# 87
# "Técnico en terapias naturales y naturopatía"
# 88
# "Ingeniería en Gestión"
# 89
# "Psicopedagogía"
# 90
# "Matemática "
# 91
# "Administración de Empresas Turísticas"
# 92
# "Geomensura / Topografía / Agrimensura"
# 93
# "Psicología Laboral"
# 94
# "Psicología"
# 95
# "Diseño de Interiores y Mobiliario"
# 96
# "MBA"
# 97
# "Ingeniería Hidráulica"
# 98
# "Licenciatura en Seguridad e Higiene en el Trabajo"
# 99
# "Ingeniería en Climatización"
# 100
# "Ingeniería Ejecución Web Manager"
# 101
# "Técnico Productor en Medios Visuales"
# 102
# "Ingeniería de Sistemas de Información Empresarial y Control de Gestión"
# 103
# "Doctorado"
# 104
# "Economía "
# 105
# "Pedagogía Media / Educación Media / Secundaria"
# 106
# "Diseño Editorial"
# 107
# "Ingeniería en Automatización y Robótica"
# 108
# "Licenciatura en Literatura / Literatura / Letras"
# 109
# "Higienista Dental"
# 110
# "Diplomado"
# 111
# "Técnico de Nivel Sup. en Guía Turístico en la Naturaleza"
# 112
# "Técnico en Mecánica Industrial"
# 113
# "Pedagogía en Matemáticas / Computación"
# 114
# "Ingeniería en Gestión Turística"
# 115
# "Bioquímica"
# 116
# "Ingeniería Civil Química"
# 117
# "Técnico de Nivel Superior en Computación"
# 118
# "Técnico en control de calidad"
# 119
# "Técnico en Laboratorio Clínico"
# 120
# "Técnico en Comercio Exterior"
# 121
# "Turismo de Aventura"
# 122
# "Ingeniería en Mecatrónica"
# 123
# "Cine / Séptimo Arte"
# 124
# "Bachillerato en Arte"
# 125
# "Pedagogía en Educación Física y Deporte"
# 126
# "Técnico en Instrumentación,Automatización y Control Industrial"
# 127
# "Tecnologías De La Información y Comunicación"
# 128
# "Ingeniería civil en minas"
# 129
# "Diseño y Producción de Areas Verdes"
# 130
# "Técnico en Electrónica y Electrónica Industrial"
# 131
# "Laboratorio Dental / Mecánica Dental"
# 132
# "Ingeniería en Agronomía"
# 133
# "Administración Pública"
# 134
# "Terapia Física"
# 135
# "Técnico en procesos industriales"
# 136
# "Estadísticas"
# 137
# "Técnico en Planificación Vial"
# 138
# "Mecánica"
# 139
# "Ingeniería en Transporte"
# 140
# "Diseño Digital"
# 141
# "Licenciatura en Ciencias Biológicas"
# 142
# "Periodismo"
# 143
# "Diseño"
# 144
# "Ingeniería civil ambiental"
# 145
# "Técnico en Instrumentación, Automatización y Control Industrial"
# 146
# "Actuación y Teatro"
# 147
# "Artes Visuales"
# 148
# "Ingeniería en Computación e Informática"
# 149
# "Técnico de Nivel Superior en Actividad Física y Deportes"
# 150
# "Fisioterapia"
# 151
# "Técnico en Climatización"
# 152
# "Ingeniería en Recursos Humanos"
# 153
# "Magister"
# 154
# "Ingeniería"
# 155
# "Licenciatura en Recursos Humanos"
# 156
# "Técnico en Minería y Metalúrgica"
# 157
# "Ingeniería en Marina Mercante"
# 158
# "Prevención de Riesgos / Seguridad Industrial "
# 159
# "Tecnología en Metalurgia"
# 160
# "Cosmetología"
# 161
# "Animación Digital"
# 162
# "Ingeniería de Diseño / Automatización Electrónica"
# 163
# "Pedagogía en Educación Diferencial"
# 164
# "Fonoaudiología"
# 165
# "Licenciatura en Química"
# 166
# "Psicología Clínica"
# 167
# "Hotelería / Administración Hotelera"
# 168
# "ADMINISTRACIÓN TURÍSTICA Y HOTELERA"
# 169
# "Ingeniería de Ejecución en Administración Hotelera"
# 170
# "Administración en Alimentación Colectiva"
# 171
# "Química y Farmacia"
# 172
# "Tecnología Médica"
# 173
# "Técnico en Mantención"
# 174
# "Construcción Civil"
# 175
# "Administración y Evaluación De Proyectos"
# 176
# "Administración de Ventas"
# 177
# "Finanzas Bancarias / Negocios Internacionales"
# 178
# "Técnico en Podología"
# 179
# "Asistente Social"
# 180
# "Ingeniería en Ejecución Mecánica"
# 181
# "Técnico en Enfermería"
# 182
# "Paisajismo / Diseño de Paisaje  "
# 183
# "Licenciatura en Matemática"
# 184
# "Contador Público y Auditor"
# 185
# "Técnico en Edificación"
# 186
# "Administración Empresas en Marketing y Comunicación Digital"
# 187
# "Ingeniería en Ordenación Ambiental"
# 188
# "Filosofía"
# 189
# "Administración de Negocios Internacionales"
# 190
# "Bibliotecología / Documentación"
# 191
# "Técnico en Comunicación Audiovisual"
# 192
# "Secretariado Bilingue"
# 193
# "Comunicación Audiovisual y/o Multimedia"
# 194
# "Ingenieria Civil en Sonido"
# 195
# "Técnico en Contabilidad General"
# 196
# "Químico Laboratista Industrial"
# 197
# "Matrón (a)"
# 198
# "Técnico / Tecnólogo / Técnico Superior"
# 199
# "Electromecánico"
# 200
# "Control de Gestión"
# 201
# "Ingeniería Industrial"
# 202
# "Técnico en Logística"
# 203
# "Pedagogía en Biología y Ciencias Naturales"
# 204
# "Técnico en Matricería"
# 205
# "Mecatrónica"
# 206
# "Ingeniería Ejecución en Gestión Industrial"
# 207
# "Fotografía"
# 208
# "Ingeniería de Petróleos / Petroquímica"
# 209
# "Psicología Educacional"
# 210
# "Técnico en Mecánica"
# 211
# "Técnico en Administración de Empresas"
# 212
# "Medicina Veterinaria"
# 213
# "Administración Hotelera Profesional"
# 214
# "Ingeniería en Refrigeración y Climatización"
# 215
# "Ingeniero Naval"
# 216
# "Pedagogía en Educación Básica"
# 217
# "Informática Biomédica"
# 218
# "Técnico de Nivel Superior en Organización y Producción de Eventos"
# 219
# "Ingeniería en Estadística"
# 220
# "Asistente Ejecutivo"
# 221
# "Periodismo Deportivo"
# 222
# "Contactología"
# 223
# "Ingeniería en Acuicultura y Pesca"
# 224
# "Antropología"
# 225
# "Creación e Interpretación Musical"
# 226
# "Geoquímica"
# 227
# "Licenciatura en Arte / Bellas Artes"
# 228
# "Técnico en Turismo y Hotelería"
# 229
# "Orientación Familiar"
# 230
# "Técnico en Prevención de Riesgos"
# 231
# "Administración gastronómica"
# 232
# "Ingeniería en Gestión y Desarrollo Tecnológico"
# 233
# "Ingeniería Civil en Energías Renovables"
# 234
# "Ingeniería en Recursos Naturales"
# 235
# "Técnico en Medio Ambiente"
# 236
# "Pedagogía en Religión"
# 237
# "Técnico en Sonido"
# 238
# "Sociología"
# 239
# "Técnico en Oleohidráulica y Neumática"
# 240
# "Administración de Empresas e Ing. Asociadas"
# 241
# "Medicina "
# 242
# "Técnico en Construcción y Obras Civiles"
# 243
# "Técnico Universitario en Telecomunicaciones y Redes"
# 244
# "Actuario"
# 245
# "Técnico en Administración de Redes y Soporte"
# 246
# "Otra carrera"
# 247
# "Electrónica"
# 248
# "Técnico Marino"
# 249
# "Técnico en Refrigeración"
# 250
# "Ciencias Políticas"
# 251
# "Técnico Financiero"
# 252
# "Pedagogía en Cs. Naturales y Química"
# 253
# "Turismo Técnico Mención Tráfico y Carga Aérea"
# 254
# "Bachiller en Ciencias Religiosas"
# 255
# "Ingenieria en Biotecnología"
# 256
# "Bachillerato en Ciencias"
# 257
# "Relaciones del Trabajo"
# 258
# "Ingeniería Geomática"
# 259
# "Ingeniería en Geomensura"
# 260
# "Técnico en Economía y Administración de la pequeñas y mediana empresa"
# 261
# "Ingeniería en Construcción"
# 262
# "Ilustración Digital"
# 263
# "Técnico en Diseño Gráfico"
# 264
# "Ingeniería Forestal"
# 265
# "Licenciatura en Ciencias Religiosas y Estudios Eclesiásticos"
# 266
# "Secretariado"
# 267
# "Ingeniería Civil en Electricidad"
# 268
# "Administración de Empresas de Servicios"
# 269
# "Cartografía"
# 270
# "Tecnología y Administración Agrícola"
# 271
# "Tecnología Pecuaria"
# 272
# "Ingeniería en Metalmecánica"
# 273
# "Ingeniería en Medio Ambiente"
# 274
# "Construcciones Metálicas"
# 275
# "TÉCNICO EN TRANSPORTE MARÍTIMO Y PUERTOS"
# 276
# "Ingeniería en Automatización y Control Industrial"
# 277
# "Técnico en Química (Análisis e Industrial)"
# 278
# "Ingenieria en RRHH"
# 279
# "Ingeniería de Ejecución en Administración Turística"
# 280
# "Doctorado Ciencias de la Educación"
# 281
# "Ingeniería Civil Eléctrica"
# 282
# "Administración De Autotransporte y Logística"
# 283
# "Informática"
# 284
# "Ingeniería en Informática / Sistemas"
# 285
# "Ingeniería en Conectividad y Redes"
# 286
# "Clasificación Arancelaria y Despacho Aduanero"
# 287
# "Artes / Artes Plásticas / Artes Gráficas"
# 288
# "Auxiliar Paramédico"
# 289
# "Técnico de Nivel Superior en Vitivinicultura y Enología"
# 290
# "Terapia Ocupacional"
# 291
# "Ingeniería en Proyectos Industriales"
# 292
# "Ingeniería en manufactura industrial"
# 293
# "Danza / Interpretación en Danza "
# 294
# "Ingeniería en Geografía"
# 295
# "Turismo Técnico Mención Empresas de Viajes"
# 296
# "Administración y Producción Agropecuaria"
# 297
# "Ingeniería en Prevención de Riesgos"
# 298
# "Ingeniería de Ejecución Industrial"
# 299
# "Traducción e Interpretación"
# 300
# "Análisis de Sistemas / Analista Programador"
# 301
# "Socioeconomía"
# 302
# "Técnico en Trabajo Social"
# 303
# "Pedagogía en Cs. Naturales y Física"
# 304
# "Dirección y Producción de eventos"
# 305
# "Administración Financiera"
# 306
# "Mantenimiento de Maquinaria de Planta"
# 307
# "Pedagogía Media en Religión y Educación Moral"
# 308
# "Comercialización"
# 309
# "Biotecnología / Bioingeniería"
# 310
# "Ingeniería en Computación"
# 311
# "Ingeniería Agropecuaria"
# 312
# "Geominería"
# 313
# "Trabajo Social"
# 314
# "Técnico asistente del educador diferencial"
# 315
# "Pastelería Internacional"
# 316
# "Técnico en geominería"
# 317
# "Ingeniería en Administración Agroindustrial"
# 318
# "Pedagogía en Lenguaje y Literatura"
# 319
# "Historia del Arte"
# 320
# "Ingeniería Civil Electrónica"
# 321
# "Ingeniería Diseño de Productos"
# 322
# "Educación Física"
# 323
# "Recursos Humanos / Relaciones Industriales"
# 324
# "Técnico en Farmacia"
# 325
# "Ingeniería en Información y Control de Gestión"
# 326
# "Administración de Hoteles y Restaurantes"
# 327
# "Ingeniería en Agronegocios"
# 328
# "Técnico agropecuario"
# 329
# "Técnico en Arte y Gestión Cultural"
# 330
# "Nutrición y Alimentación Institucional"
# 331
# "Técnico en Tránsito y Transporte"
# 332
# "Ingeniería Mecánica"
# 333
# "Venta y Publicidad"
# 334
# "Administración Industrial"
# 335
# "Procesos Agroindustriales"
# 336
# "Técnico en peluquería y estética"
# 337
# "Asistente Judicial"
# 338
# "Ingeniería en Marketing"
# 339
# "Licenciatura en Educación / Magisterio"
# 340
# "Ingeniería en Bioprocesos"
# 341
# "Técnico en Electricidad y Electricidad Industrial"
# 342
# "Ingeniería Civil en Minas"
# 343
# "Ingeniería en Telemática"
# 344
# "Diseño y Producción Industrial"
# 345
# "Licenciatura en Ciencias del Medio Ambiente"
# 346
# "Relaciones Públicas"
# 347
# "Técnico Veterinario"
# 348
# "Ingeniería Agrícola"
# 349
# "Técnico en Topografia"
# 350
# "Ingeniería en Mantenimiento Industrial"
# 351
# "Obstetricia y Puericultura"
# 352
# "Ingeniería en transporte marítimo"
# 353
# "Técnico Dental y Asistente de Odontología"
# 354
# "Contador Auditor"
# 355
# "Ingeniería en Ejecución Electrónica"
# 356
# "Ingeniería en Construcción Civil"
# 357
# "Ingeniería Civil en Computación e Informática"
# 358
# "Técnico en Servicio Social"
# 359
# "Publicidad"
# 360
# "Ingeniería Mecánica en Producción Industrial"
# 361
# "Comunicación Social / Empresarial"
# 362
# "Ingeniería Civil en Agroindustrias"
# 363
# "Preparador Físico"
# 364
# "Administración Gastronómica Internacional"
# 365
# "Química Industrial"
# 366
# "Técnico de Radiología y Radioterapia"
# 367
# "Ingeniería de Ejecución en Mecánica Automotriz y Autotrónica"
# 368
# "Ingeniería en Física"
# 369
# "Sistemas de Gestión de la Calidad"
# 370
# "Ingeniería Civil Metalúrgica"
# 371
# "Programación"
# 372
# "Administrador Universitario de Empresas"
# 373
# "Ciencias Físicas"
# 374
# "Técnico en Electricidad Industrial"
# 375
# "Técnico en Salud Natural y Terapias Complementarias"
# 376
# "Microbiología industrial de alimentos"
# 377
# "Marketing"
# 378
# "Ingeniería Civil Industrial"
# 379
# "Paramédico"
# 380
# "Astronomía"
# 381
# "Conservación Industrial de Alimentos por Frío"
# 382
# "Tecnología en Minería y Metalurgía"
# 383
# "Tecnólogo / Técnico Control Industrial"
# 384
# "Ingenieria en Comercio / Negocio Internacional"
# 385
# "Ingeniería Matemáticas"
# 386
# "Técnico en Comunicación para las Organizaciones Sociales"
# 387
# "Tecnología y Administración Pecuaria"
# 388
# "Ingeniería en Ejecución Eléctrica"
# 389
# "Ingeniería Civil"
# 390
# "Química"
# 391
# "Técnico en Deporte, Recreación y Preparación Física"
# 392
# "Dibujo y Proyectos Industriales"
# 393
# "Diseño de Vestuario"
# 394
# "Biología en Gestión de Recursos Naturales"
# 395
# "Ingeniería de Producción"
# 396
# "Física / Ciencias Físicas"
# 397
# "Ingeniería Comercial"
# 398
# "Ingeniería en Aviación Comercial"
# 399
# "Ingeniería Aerospacial / Aeronáutica"
# 400
# "Agronomía"
# 401
# "Electrónica de Sistemas Computarizados"
# 402
# "Diseño Gráfico"
# 403
# "Maestría en Dirección Comercial"
# 404
# "Ingeniería Biomédica"
# 405
# "Producción Musical"
# 406
# "Pedagogía en Español"
# 407
# "Ingeniería Civil Mecánica"
# 408
# "Técnico Profesional Archivero"
# 409
# "Técnico en Gestión y Control de calidad"
# 410
# "Técnico de Nivel Superior en Bioprocesos Industriales"
# 411
# "Diseño Industrial"
# 412
# "Diseño de Objetos y Ambientes"
# 413
# "Técnico en Mantenimiento Industrial"
# 414
# "Magister en Ciencias de la Educación"
# 415
# "Técnico en traducción e interpretariado"
# 416
# "Ingeniería Química"
# 417
# "Diseño de Interiores / Decoración"
# 418
# "Dibujo de Proyectos de Arquitectura e Ingenieria"
# 419
# "Dibujo Técnico"
# 420
# "Técnico en Geomensura"
# 421
# "Ingeniería Computación Informática y Comunicaciones"
# 422
# "Ingeniería Bioquímica"
# 423
# "Geografía"
# 424
# "Licenciatura en Filosofía"
# 425
# "Ingeniería en Electricidad"
# 426
# "Pedagogía"
# 427
# "Pedagogía en Educación de Párvulos"
# 428
# "Ingeniería Civil Matemática"
# 429
# "Administración de Procesos Productivos"
# 430
# "Técnico En Bienestar Social"
# 431
# "Administración Hotelera Internacional"
# 432
# "Enfermería"
# 433
# "Servicios  Posventa Área Automotriz"


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
    



