import re

sector = {
    "AppDev": [
        'FullStack',
        'GameDev',
        'Mobile',
        'Backend',
        'Frontend',
        'AppDev'
    ],
    "AI+Research": [
        'Data Scientist',
        'Data Engineer',
        'Data Analyst',
        'MLEngineer',
        'SEO',
        'IoT',
        'AI+Research'
    ],
    "Infra": [
        "DevOps",
        "Cybersecurity",
        "CloudEngineer",
        "DBA",
        "QA",
        "Infra"
    ],
    "Blockchain": [
        "BlockchainDev"
    ],
    "Designer": [
        "Designer"
    ],
    "IT Leander": [
        "IT Leander"
    ]

}

kind = {
    'FullStack': '|'.join([
        r'full{0,2}[\s\-\_]*stac{0,2}k{0,2}',
        r'(?:react|angular|vue){1}.*(?:\.net|c#|python)',
        r'(?:\.net|c#|python|go|golang|c\+\+|php){1}.*(?:react|angular|vue){1}',
    ]),
    'Backend': '|'.join([
        r'bac{0,1}k{0,1}[\s\-\_]*end',
        r'api.*(?:develop|engine|program|architect|specialist){1}',
        r'Program[mer]{0,1}.{0,5}api'
    ]),
    'Frontend': '|'.join([
        r'fr{0,1}ont[\s\-\_]*end',
        r'(?:ux|ui|ui/ux|ux/ui){1}.*(?:develop|engine|program|architect|specialist){1}',
        r'(?:especialist|ingenier|desarrollad|arquitect){1}.*(?:ux|ui|ui/ux|ux/ui){1}',
        r'(?<!\w|\d)react[\s\-\_]*developer',
        r'(?<!\w|\d)angular[\s\-\_]*developer',
        r'(?<!\w|\d)vue[\s\-\_]*developer',
    ]),
    'Mobile': '|'.join([
        r'mobile|movil|móvil|mobil|móbil',
        r'(?<!\w|\d)(?:android|ios|flutter|appel){1}(?!\w|\d)',
        r'(?<!\w|\d)react.*(?:native|nativo){1}'

    ]),
    'GameDev': '|'.join([
        r'gam{1,2}e.*(?:develop|program){1}',
        r'(?:desarrollad|programad){1}.*juego'
    ]),
    'AppDev': '|'.join([
        r'(?:especialist|ingenier|desarrollad|arquitect){1}.*web',
        r'web.*(?:develop|engine|program|architect|specialist){1}',
        r'develop|programad|programmer|desarrollad|dezarrollad',
        r'software|application|system',
        r'sistemas|aplicaciones',
        r'solutions.*architect',
        r'Arquitect.*Solucione',
        r'python|c#|c\+\+|java|javascript|typescript|ruby|haskell|scala|golang|node[\s\_\-\.]*js|visual[\s\_\-]*basic|\.[\s\_\-]*Net',
        r'(?<!\w|\d)ts(?!\w|\d)',
        r'(?<!\w|\d)js(?!\w|\d)',
        r'(?<!\w|\d)go(?!\w|\d)',
        # r'(?:python|c#|.Net|Go|golang|TS|JS|JavaScript|TypeScript){1}.*(?:develop|engine|program|specialist){1}',
        # r'(?:desarrollad|ingenier|programad|especialista){1}.*(?:python|c#|.Net|Java){1}'
    ]),
    'Data Scientist': '|'.join([
        r'(?<!big[\s\-\_]{1})data.*(?:science|scientist){1}',
        r'[c|s]ient[i|í]fic.*dat[o|a]{1}'
    ]),
    'Data Engineer': '|'.join([
        r'(?<!big[\s\-\_]{1})data[\s\-\_]*(?:engine|architect|model|specialist)',
        r'(?:in[g|j]enier|arquitect).*dat[o|a]{1}',
        r'etl|elt|spack|hadoop',
        r'Data[\s\-\_]*Ops',
        r'ML[\s\-\_]*Ops',
    ]),
    'Data Analyst': '|'.join([
        r"(?<!big[\s\-\_]{1})data.*analys{0,1}t",
        r"analista.*(?<!big[\s\-\_]{1})dat[o|a]{1}",
        r'business.*(?:intelligence|analyst|strategist|develop){1}',
        r'(?<!\w|\d)bi[\s\-\_]+.*(?:develop|engine|analyst){1}',
        r'(?:desarrollad|ingenier|analista){1}.*(?<!\w|\d)bi(?!\w|\d)',
        r'inteligencia.*negocio',
    ]),
    'MLEngineer': '|'.join([
        r'(?:machine|deep){1}.*learning',
        r'computer.*vision',
        r'speech.*recognition',
        r'aprendi[z|s]{1}aje.*(?:m[a|á]{1}quina|autom[a|á]{1}tico|profundo){1}',
        r'vi[s|c]{1}i[o|ó]{1}n.*computadora',
    ]),
    'SEO': '|'.join([
        r'SEO.*(?:Specialist|Analyst|Engine|Strategist){1}',
        r'(?:especialist|ingenier){1}.*SEO',
        r'search.*engine.*optimization'
    ]),
    'IoT': '|'.join([
        r'IoT.*(?:Engine|architect|specialist|security){1}',
        r'Internet of Things',
        r'(?:Ingenier|arquitect|especialista){1}.*IoT',
    ]),
    'AI+Research': '|'.join([
        r"big.*data",
        r'artificial.*intelligence',
        r'(?:ia|ai){1}.*(?:engine|research){1}',
        r'(?:ingenier|investigad){1}.*(?:ia|ai){1}',
        r'inteligencia.*artificial',
        r'genetic.*algorithm',
        r'predictive.*modeling',
        r'data.*visualization',
        r'[v|b]{1}isuali[z|s]{1}aci[o|ó]{1}n.*dato',
        r'data.*classification'
    ]),
    "DevOps": '|'.join([
        r'Dev[\s\-\_]*Ops',
        r'Dev[\s\-\_]*Ops[\s\-\_]*Sec',
        r'Dev[\s\-\_]*Sec[\s\-\_]*Ops',
        r'Virtual.*Infrastructure',
        r'Virtualization|Virtualizaci[o|ó]n',
        r'automati[z|s]aci[o|ó]{1}n.*despliegues',
        r'deploy.*automation',
        r'Server.*Administrator',
        r'administrad.*servidor',
        r'Ingenier.*Host'
    ]),
    "Cybersecurity": '|'.join([
        r'cybersecurity',
        r'information.*security',
        r'network.*security',
        r'cloud.*security',
        r'it.*security',
        r'Hacker',
        r'Penetration.*Tester',
        r'Security.*(?:Analyst|engine|architect|specialist)',
        r'ciberseguridad',
        r'seguridad.*(?:informática|información)',
        r'(?:Analista|Ingenier|Especialista|arquitect).*[b|v]{1}ulnera[b|v]{1}ilidades',
        r'(?:Analista|Ingenier|Especialista|arquitect).*Seguridad'
    ]),
    "CloudEngineer": '|'.join([
        r'cloud.*(?:Architect|Engine|Develop|Specialist|Migration|Infrastructure|support|services|consultor){1}',
        r'(?:Arquitect|Ingenier|Especialista|Desarrollad|Infraestructura|administra|consult){1}.*(?:cloud|nube){1}',
        r'Azure|Aws|Cloud[\s\-\_]*Ops'
    ]),
    "DBA": '|'.join([
        r'(?<!\w|\d)DBA(?!\w|\d)',
        r'(?:Database|System){1}.*(?:Administrator|Manager){1}',
        r'Database.*(?:Develop|Engine|architect|specialist){1}',
        r'(?:Administrad|Gest).*(?:sistemas|base.*dato)',
        r'(?:Desarrollad|Ingenier|arquitecto|especialista).*base.*dato'
    ]),
    'QA': '|'.join([
        r'(?<!\w|\d)QA(?!\w|\d)',
        r'(?<!\w|\d)SDET(?!\w|\d)',
        r'Qualit[y|i]{1}.*(?:As{1,2}urance|Engineer)',
        r'Tester',
        r'Quantitative.*(?:Analyst|Develop){1}',
        r'Automation.*(?:develop|engine|specialist)',
        r'(?:Especialista|Analista|Ingenier|desarrollad){1}.*prueba',
        r'(?:Especialista|Analista|Ingenier|desarrollad){1}.*calidad.*software',
        r"testing.*(?:specialist|engine|develop|architect|analyst){1}",
        r'software.*quality',
        r'Automatizad',
        r'[b|v]{1}erifica[s|c]{1}i[o|ó]{1}n.*[v|b]{1}alida[s|c]{1}i[o|ó]{1}n',
        r'verification.*validation',
    ]),
    "Infra": '|'.join([
        r'network.*(?:administrat|engine|analyst|architect|specialist)',
        r'configuration.*(?:administrat|engine|analyst|architect|specialist|manager)',
        r'(?:administra|ingenier|analista|arquitect|especialista|T[e|é]cnicos).*red',
        r'(?:administra|ingenier|analista|arquitect|especialista|manager).*configuraciones',
        r'Networking|Infraestructura|Infraestructure'
    ]),
    "Designer": '|'.join([
        r'Designer|Animador|Diseñad',
    ]),
    "BlockchainDev": '|'.join([
        r'Blockchain|Solidity|Ethereum|Bitcoin|Solana'
    ]),
    "IT Leander": '|'.join([
        r'pro[j|y]{1}ect.*manager',
        r'(?:IT|Software|Technical){1}.*coordinator{1}',
        r'(?:team|Technical){1}.*lead',
        r'Scrum.*Master|Chief.*Technology.*Officer|(?<!\w|\d)cto(?!\w|\d)|Director.*Technology',
        r'(?:Gerente|Coordinad).*(?:TI|IT|tecnol|software)',
        r'Principal.*(?:software|engine|develop)',
        r'(?:Ingenier|desarrollad).*principal',
        r'(?:l[i|í]{1}der|jefe).*(?:pro[y|j]{1}ecto|equipo|t[e|é]{1}cnico|desarrollo)',
        r'Direct.*tecnol',
        r'Agile.*Coach',
        r'Tech.*Lead'
    ]),
}

for s in [
    'Backend Developer',
    'Backend Engineer',
    'Back-End Architect',
    'API Programmer',
    'Desarrollador/a back-end',
]:
    name = 'Backend'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), s


for s in [
    'Frontend Developer',
    'Frontend Engineer',
    'Front-End Architect',
    'Front-End Developer',
    'FontEnd',
    'UI/UX Developer',
    'UI/UX Architect',
    'UX/UI specialist',
    'UI Developer',
    'Especialista en UX/UI',
    'Desarrollador/a front-end',
    'Ingeniero UX',
    'React Developer',
    'Angular Developer',
    'Vue Developer',
]:
    name = 'Frontend'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), s


for s in [
    'Full Stack Web Developer',
    'Full-stack Developer',
    'Full-stack Architect',
    'Desarrollador/a full-stack',
]:
    name = 'FullStack'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)


for s in [
    'Mobile Developer',
    'Mobile App Developer',
    'Mobile Web Developer',
    'Mobile Application Architect',
    'Android Developer',
    'Desarrollador/a de aplicaciones móviles',
    'Arquitecto/a de aplicaciones móviles',
    'IOS',
    'Android',
    'Flutter',
    'React Native',
]:
    name = 'Mobile'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    'Game Developer',
    # 'Mobile Game Developer',
    'Game Programmer',
]:
    name = 'GameDev'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)


for s in [
    'Web Developer',
    'Web Analytics Developer',
    'Web Application Developer',
    'Web Engineer',
    'Desarrollador Web',
    "Virtual Reality Developer"
    'Software Engineer',
    'Solutions Architect',
    'Software Architect',
    'Software Development Manager',
    'Software Developer',
    'Systems Engineer',
    'Web Development Manager',
    'Application Developer ',
    'Software Development Engineer',
    'Software Engineering Manager',
    'Ingeniero/a de software',
    'Ingeniero/a de sistemas',
    'Desarrollador/a de aplicaciones',
    'Analista programador/a',
    'Programmer analyst',
    'Desarrollador/a de comercio electrónico',
    'e-commerce developer',
    'Python Engineer',
]:
    name = 'AppDev'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    'Data Scientist',
    'Científico/a de datos',
    'Científico/a de datos de inteligencia artificial',
    'artificial intelligence data scientist',
    'Data Science',
]:
    name = 'Data Scientist'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    'Data Engineer',
    'Data Architect',
    'Ingeniero/a de datos',
    'Arquitecto/a de datos',
    'Data Modeler',
    'ETL',
]:
    name = 'Data Engineer'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "Machine Learning Engineer",
    "Computer Vision Engineer",
    "Machine Learning Researcher",
    "Speech Recognition Engineer",
    "Machine Learning Technician ",
    "Ingeniero/a de machine learning",
    "Ingeniero/a de visión por computadora",
    # "Científico/a de datos de aprendizaje profundo",
    # "Deep learning data scientist",
]:
    name = 'MLEngineer'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "Data Analyst",
    "Analista de datos",
    "Business Intelligence Analyst ",
    "Business Analyst",
    "Business Systems Analyst",
    "Business Intelligence Developer ",
    "Business Intelligence Architect",
    "IT Business Strategist",
    "Business development executive",
    "Business Analyst",
    "Business Intelligence",
    "inteligencia negocio",
    "BI Develope",
    "BI Engineer",
    "BI Developer",
    "Business Intelligence analyst",
    "Analista de BI",
]:
    name = 'Data Analyst'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "SEO Specialist",
    # "Digital Marketing Specialist",
    # "Social Media Manager",
    # "Content Strategist",
    "Search Engine Optimization (SEO) Analyst",
    "Especialista en SEO",
    "SEO specialist",
]:
    name = 'SEO'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "IoT (Internet of Things) Engineer",
    "Ingeniero/a de IoT",
    "IoT engineer",
    "Arquitecto/a de soluciones de IoT",
    "IoT solutions architect",
    # "Especialista en seguridad de IoT",
    # "IoT security specialist",
]:
    name = 'IoT'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "Big Data Engineer",
    "Big Data Analyst",
    "Analista de Big Data",
    "Artificial Intelligence Specialist ",
    "AI (Artificial Intelligence) Engineer",
    "Genetic Algorithm Designer",
    "Predictive Modeling Specialist",
    "Investigador/a de inteligencia artificial",
    "AI researcher",
    "Especialista en visualización de datos",
    "Data visualization specialist",
]:
    name = 'AI+Research'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)


for s in [
    "DevOps Engineer",
    "DevSecOps Engineer",
    "Virtual Infrastructure Engineer",
    "Virtualization Engineer",
    "Server Administrator",
    "Ingeniero/a DevOps",
    "DevOps engineer",
    "Especialista DevOps",
    "DevOps specialist",
    "Ingeniero/a de automatización de despliegues",
    # "deployment automation engineer",
    "DevOpsSec",
    "Ingeniero en Despliegue y Virtualización",

]:
    name = 'DevOps'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "Cybersecurity Analyst",
    "Information Security Analyst",
    "Network Security Engineer",
    # "Cloud Security Specialist",
    "Growth Hacker",
    "IT Security Specialist ",
    "Cybersecurity Consultant",
    "Information Security Manager",
    # "Penetration Tester",
    "Web Security Analyst",
    "Security Analyst",
    "Especialista en ciberseguridad",
    "cybersecurity specialist",
    "Analista de seguridad informática",
    "information security analyst",
    "Ingeniero/a de seguridad de la información",
    "information security engineer",
    "Cybersecurity Engineer",
    "Ciberseguridad",
    "Security Analyst",
    "Security Engineer",
    "Analista Vulnerabilidades",
    "Analista Seguridad",
    "Ingeniero Seguridad",
]:
    name = 'Cybersecurity'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "Cloud Architect",
    "Cloud Engineer",
    "Cloud Developer",
    "Cloud Solutions Architect",
    "Cloud Migration Specialist",
    "Cloud Migration Engineer",
    "Cloud Infrastructure Architect",
    "Arquitecto/a de soluciones en la nube",
    "Ingeniero/a de soporte en la nube",
    "cloud support engineer",
    "cloud services specialist",
    "Especialista en servicios en la nube",
    "Ingenier Cloud,",
    "Arquitect Cloud",
    'Administrador Cloud'
]:
    name = 'CloudEngineer'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "Database Administrator",
    "System Administrator",
    "Database Developer",
    "Administrador/a de sistemas",
    "Gestor/a de bases de datos",
    "Administrador/a de bases de datos",
    "Programación - especialista en manejo de base de datos"
]:
    name = 'DBA'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "QA Engineer",
    "Quality Assurance Manager",
    "Software Quality Assurance (QA) Tester",
    "Performance Tester",
    "Quantitative Analyst",
    "SDET (Software Development Engineer in Test)",
    "QA Automation Engineer",
    "Quantitative Developer",
    "Software Tester ",
    "software QA engineer",
    "Ingeniero/a de calidad de software",
    "Especialista en pruebas",
    "testing specialist",
    "Analista de pruebas",
    "testing analyst",
    "Especialista en control de calidad de software",
    "Software quality control specialist",
    "Especialista en verificación y validación de software",
    "Software verification and validation specialist",
    "QA",
    "Automation Engineer",
    "Automatizador",
    "Quality Engineer"
]:
    name = 'QA'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "Network Administrator",
    "Network Engineer",
    "Network Analyst ",
    "Wireless Network Engineer ",
    "Computer Network Architect",
    "Configuration Manager/Engineer",
    "Network Support Specialist",
    "Ingeniero/a de redes",
    "Arquitecto/a de redes",
]:
    name = 'Infra'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "UX/UI Designer",
    "Web Designer",
    "User Interface (UI) Designer",
    "Game Designer",
    "3D Graphic Designer",
    "UI Designer ",
    "Diseñador/a web",
    "Animador/a 3D",
    "Diseñador/a de experiencia de usuario",
    "User experience designer",
    "Diseñador/a de interacción",
    "Interaction designer",
    "Diseñador/a de interfaz",
    "Interface designer",
]:
    name = 'Designer'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "Blockchain Developer",
    "Blockchain Analyst",
    "Desarrollador/a de blockchain",
    "Especialista en tecnología blockchain",
    "blockchain technology specialist",
    "Arquitecto/a de soluciones blockchain",
    "blockchain solutions architect",
]:
    name = 'BlockchainDev'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

for s in [
    "IT project manager",
    "Project Manager",
    "Software project coordinator",
    "IT Team Lead",
    "Technical Lead",
    "development team leader",
    "Scrum Master",
    "Chief Technology Officer (CTO)",
    "Director of Technology",
    "Technical Project Coordinator",
    "Gerente de proyectos de TI",
    "Gerente de proyectos tecnológicos",
    "Coordinador/a de proyectos de software",
    "Coordinador/a de IT",
    "Principal Software Engineer",
    "Director/a de tecnología",
    "Líder técnico de proyectos",
    "Jefe de equipo de desarrollo",
    "Agile Coach",
    "Lider Tecnico",
    "Lider Técnico",
]:
    name = 'IT Leander'
    assert re.search(kind[name], s, re.IGNORECASE), s
    for key in kind.keys():
        if key in [name] + list(sector.keys()):
            continue
        assert not re.search(kind[key], s, re.IGNORECASE), (s, key)

"""\

Others:
  - Especialista en SEM
  - Content marketing specialist
  - Especialista en marketing de contenidos
  - Especialista en marketing digital
  - SEM specialist
  - Digital marketing specialist





  - Analista de sistemas informáticos
  - Técnico/a de hardware
  - hardware technician

  - Product Analyst
  - Technical Writer
  - Tech Support Specialist
  - Technical Support Engineer
  - Technical Support Specialist
  - Help Desk Technician
  - Mobile Device Manager
  - IT Manager
  - Product Manager



  - Information Systems Manager

  - IT Service Manager
  - Digital Product Manager
  - Incident Manager
  - Technical Account Manager 

  - IT Consultant
  - Augmented Reality Developer
  - E-commerce Specialist
  - Technical Sales Representative
  - Product Owner
  - IT Auditor
  - IT Operations Manager
  - IT Procurement Manager
  - Technical Program Manager
  - Robotics Engineer
  - Systems Analyst
  - Technical Operations Manager
  - Enterprise Architect
  - Computer Systems Analyst
  - IT Sales Representative 
  - Product Marketing Manager 
  - Technical Marketing Engineer 
  - Sales Engineer 
  - Cryptographer 
  - Digital Forensic Analyst
  - Enterprise Systems Engineer
  - Over-The-Top (OTT) Specialist
  - Red Team Engineer 
  - Software Operations Engineer
  - Telecom Network Architect
  - AR/VR Developer
  - Digital Analyst
  - e-Commerce Manager
  - Growth Analyst
  - IT Architect 
  - IT Auditor 
  - IT Support Technician 


  - Technical Writer/Editor 
  - Technology Analyst
  - User Researcher
  - Video Game Producer 
  - Web Content Manager 
  - Workforce Management Analyst
  - CRM Specialist 
  - Technical Recruiter
  - IT Trainer
  - IT Technical Recruiter
  - Growth Marketing Manager
  - Inductive Reasoning Specialist
  - IT Operations Technician
  - IT Service Desk Manager
  - IT Service Delivery Manager
  - Salesforce Administrator
  - Site Reliability Engineer (SRE) 
  - Social Media Strategist
  - Technical Program Manager
  - Technical Recruiter
  - Technical Sales Specialist
  - Technical Solution Architect
  - Technical Support Analyst
  - Usability Specialist
  - Ingeniero/a de telecomunicaciones
  - telecommunications engineer


  - Técnico/a de soporte de IT
  - IT support technician
  - Administrador/a de sistemas de IT
  - IT system administrator
  - Especialista en redes y telecomunicaciones
  - network & telecommunications specialist
  - Arquitecto/a de información
  - Information architect
  - Especialista en redes sociales
  - Social media specialist
  - Coordinador/a de marketing de redes sociales
  - Social media marketing coordinator
  - Especialista en gestión de comunidades
  - Community management specialist
  - Gerente de cuentas
  - Account manager
  - Especialista en ventas de soluciones tecnológicas
  - Technology solutions sales specialist
  - Especialista en documentación técnica
  - Technical documentation specialist
  - Redactor/a técnico/a
  - Technical writer
  - Especialista en contenido técnico
  - Technical content specialist
  - Especialista en robótica
  - Robotics specialist
  - Editor/a de contenidos web
  - Web content editor
  - Especialista en email marketing
  - Email marketing specialist
  - Autor/a de contenido digital
  - Digital content writer
  - Especialista en comercio electrónico
  - E-commerce specialist
  - Gerente de ventas en línea
  - Online sales manager
  - Analista de datos de ventas en línea
  - Online sales data analyst
  - Instructor/a de software
  - Software instructor
  - Especialista en capacitación técnica
  - Technical training specialist
  - Gerente de programas de entrenamiento técnico
  - Technical training program manager
"""


def detect_kind_of_job(title):
    result, sectors = [], set()
    for s, kinds in sector.items():
        for key_kind in kinds:
            if matches := re.findall(kind[key_kind], title, re.IGNORECASE):
                assert '' not in matches, (title, key_kind)
                result.append(key_kind)
                sectors.add(s)
                break

    return result, sectors
