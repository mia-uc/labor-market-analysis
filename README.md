## Motivación

En las últimas décadas, el mercado laboral ha evolucionado significativamente moviéndose desde los métodos
tradicionales de publicidad en periódicos y tablones de anuncios hacia una presencia dominante en la web.
Actualmente, existen numerosos sitios web dedicados a la publicación de ofertas de trabajo y la búsqueda de
candidatos calificados para llenar esos cargos vacantes. A estos sitios también se suman las páginas de las
empresas, donde las misma publican de sus ofertas de empleo.

En un mundo cada vez más enfocado en la tecnología, dicho sector representa una proporción muy
significativa dentro de este mercado laboral. Con la creciente adopción de prácticas como el trabajo remoto,
la computación en la nube y otras tecnologías emergentes, la demanda de habilidades tecnológicas y la exigencia
de los empleadores sigue aumentando día a día.

En este contexto, es vital que las personas que buscan empleo en el sector tecnológico tengan una comprensión
clara y actualizada de las tendencias y oportunidades actuales.

## Objetivos

El objetivo de este trabajo es analizar el mercado laboral actual a partir de sus datos. Respondiendo preguntas como ¿Cual es el puesto de trabajo más demandado?, ¿Cuales son las habilidades más demandados?, ¿Cuales son los sectores mejor pagados? o ¿Cuales son los sectores más exigentes?. Aunque la lista de preguntas y respuestas finales dependerán de la información concreta que se encuentre en los datos. Además, se busca clasificar y seleccionar las ofertas de trabajo que mejor coincidan con un perfil determinado. Por último, se pretende determinar cuáles son las habilidades recomendables que deben ser adquiridas para completar un perfil específico y aspirar a un puesto de trabajo determinado. Este estudio proporcionará información valiosa a los individuos que buscan trabajo así como a las empresas que buscan contratar y retener talentos.

## Fuente de Datos

En este casos nuestra fuente de datos serian las múltiples páginas de la web que anuncian ofertas de empleo del sector y región seleccionados para el estudio. A continuación se muestra una lista de ejemplos (coleccionados sin catalogar, la lista definitiva será una lista más selectiva en la cual se acote la región de interés):

- https://www.getonbrd.com
- https://www.infojobs.net/candidate/my-infojobs.xhtml?dgv=6385115882063679988
- https://www.kitempleo.cl/
- https://www.opcionempleo.cl/
- https://www.airavirtual.com/portales
- https://www.tecnoempleo.com/
- https://remoteok.com/
- https://www.chiletrabajos.cl/
- https://developers.turing.com/dashboard/turing_test
- https://careers.gradiant.org/connect/dashboard
- https://whoishiring.io/search/40.4637/-3.7492/5.0000?time=now-7d
- https://jobs.smartrecruiters.com/
- https://www.aliantec.com/busquedas-activas/
- https://www.getmanfred.com/es/portal
- https://app.goboon.co/home
- https://cl.talent.com/jobs
- https://soaint.hiringroom.com/jobs?source=opcionempleo
- https://flexjobs.com
- https://whoishiring.io
- https://remoteml.com
- https://freelancer.com
- https://simplyhired.com
- https://freshersworld.com
- https://weworkremotely.com
- https://upwork.com
- https://remoteok.io
- https://devsnap.io
- https://remote.co
- https://dice.com
- https://angel.co

## Tareas

- Extracción de la información: El objetivo particular de esta etapa es la extracción de información de las páginas web, donde se pueden utilizan dos enfoques:

  - Scraper: Consiste en extraer información a partir de la estructura HTML de una página web. Este enfoque puede presentar problemas cuando el paginado del sitio no se realiza mediante cambios de url sino que en su lugar realizan un re-rendereado con mayor información tras la ejecución de un botón. En este casos dicha pagina no podrá ser analizada de manara automática sino que sera necesario la descarga manual de las distintas paginas.
  - Detección de APIs públicas o seudo-públicas: En ocasiones se puede revisar las referencias de las paginas para detectar las apis que estas consumen. Esto permitiría la extracción de datos de forma más estructurada y automatizada. El problema en este casos es que dichas apis no presenta una documentación por lo que en ocasiones puede ser complejo interactuar con esta o replicar sus protocolos de seguridad
  - Extracción Semi-automática: En el casos en que ninguno de los enfoques anteriores sean aplicables para alguna de las fuentes en concreto se puede realizar una extracción semi-automática. Este enfoque consta de dos partes, una descarga manual de contenidos HTML para su posterior análisis automático. 
  
- Limpieza de la información: El segundo objetivo particular es llevar a cabo la limpieza de los datos extraídos, lo que implica la identificación de dos entidades principales: "skills" o habilidades, y "puestos de trabajo". Además, se abordará el problema de la sinonimia y la sensibilidad a mayúsculas y minúsculas. En esta fase también se debe tener en cuenta el problema de la generalización y la particularizarían, por ejemplo casos como Backend Developer y NodeJs Backend Developer, en este ejemplo se puede considerar, a priori, dos enfoques 1) hay dos puestos de trabajos distintos, lo cual es poco preciso pues en principio uno es subconjunto del otro 2) hay un puesto de trabajo, dos ofertas, y una de ellas especifica un skill requerido

- Análisis estadísticos: El siguiente paso es realizar un estudio estadístico de la información extraída.
  El análisis estadístico tiene como objetivo extraer información relevante del mercado laboral, como:

  - ¿Cuáles son los puestos de trabajo más demandados actualmente? - Esta pregunta se puede responder mediante el análisis de cuántas veces aparece cada puesto de trabajo en las ofertas analizadas.
  - ¿Qué habilidades son las más deseadas o demandadas para un puesto de trabajo específico? - Esta pregunta se puede responder mediante el análisis de las habilidades más frecuentes asociadas con ciertos puestos de trabajo.
  - ¿Qué habilidades se requieren con más frecuencia para un puesto de trabajo específico? - Esta pregunta se puede responder mediante el análisis de las habilidades necesarias para un puesto de trabajo en particular y determinar las habilidades más importantes.
  - ¿Cuál es el rango de salario para puestos de trabajo específicos? - Esta pregunta se puede responder mediante el análisis de la distribución de los salarios de los puestos de trabajo identificados y la identificación de valores máximos, mínimos y promedios.
  - ¿Cuáles son las empresas que ofrecen los puestos de trabajo más demandados? - Esta pregunta se puede responder mediante el análisis de las empresas cuyas ofertas de trabajo se ajustan a los criterios establecidos y la determinación de qué empresas tienen una mayor presencia en el mercado.

  Por último, el análisis estadístico también puede ayudar en la identificación de patrones emergentes y contribuir a la toma de decisiones fundamentadas en el futuro del mercado laboral.

- Modelos Predictivos: Los modelos predictivos pueden ser muy útiles para cumplir con los objetivos establecidos anteriormente, aunque llegados a este punto de la investigación las preguntas finales dependerán de los datos, su cantidad, su calidad y su información. Estos son algunos ejemplos de posibles usos de modelos predictivos:

  - Predicción de la demanda futura de ciertos puestos de trabajo: Un modelo predictivo puede ser utilizado para predecir la demanda futura de ciertos puestos de trabajo, lo que puede ayudar a individuos y empresas a adquirir las habilidades necesarias para satisfacer esa futura demanda.
  - Predicción del salario esperado para ciertos puestos de trabajo: Se puede utilizar un modelo predictivo para predicción de los posibles salarios asociados con ciertos tipos de puestos de trabajo, permitiendo a los trabajadores y empleadores planear mejor a largo plazo.
  - Identificación de habilidades que se están volviendo más importantes en el mercado: Un modelo predictivo puede ser utilizado para identificar las habilidades que se están volviendo más importantes en el mercado, lo que puede permitir a los trabajadores mejorar sus habilidades y estar mejor preparados para el futuro.
  - Identificación de empresas con más probabilidades de emplear candidatos con un cierto perfil: Utilizando una base de datos de empleadores, se puede utilizar un modelo predictivo para identificar empresas con mayor probabilidad de contratar candidatos con un cierto perfil, lo que permite a los candidatos enfocar sus esfuerzos de búsqueda de empleo en las empresas más adecuadas.
  - Recomendación de skills: se pretende determinar cuáles son las habilidades recomendables que deben ser adquiridas para completar un perfil específico y aspirar a un puesto de trabajo determinado.

  En general, los modelos predictivos pueden ser una herramienta poderosa para aprovechar al máximo la información recopilada en el análisis del mercado laboral y proporcionar una mejor comprensión del mismo.
