<!-- converted from Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx -->

Arquitectura y diseño del backend para la evaluación agrícola en Huaura
Documento de referencia para el desarrollo y despliegue de la aplicación
Versión 2 • Evaluación multicultivo • 10 de septiembre de 2026
## Propósito y decisión principal
La aplicación permitirá registrar una parcela dentro de Huaura, comprobar la cobertura de sus datos geoambientales, seleccionar uno o varios cultivos para una misma evaluación y consultar resultados con evidencia trazable. CropSuiteLite será el motor de cálculo detrás de un adaptador. El backend administrará los usuarios, las parcelas, las solicitudes, la ejecución y la presentación de resultados.
La arquitectura adoptada como dirección de trabajo es un monolito modular organizado por bounded contexts, con capas Domain, Application, Infrastructure e Interfaces dentro de cada contexto. Los cálculos se ejecutarán mediante un worker separado del proceso que atiende HTTP. Esta separación permite mantener la aplicación disponible durante una evaluación y conservar las responsabilidades del modelo científico.
El despliegue inicial concentrará backend, worker y cola en un único servidor virtual económico. El frontend puede usar Vercel y la base de datos puede usar Supabase con PostgreSQL y PostGIS. El presupuesto orientativo discutido es de US$15 a US$20 mensuales para una primera aplicación pública pequeña, sujeto a medir el consumo y confirmar los cargos del proveedor.
## Estado de las decisiones

La comprobación del pipeline no equivale a una validación agronómica de campo. La aptitud estimada debe interpretarse según la resolución, el escenario y la calidad de los datos disponibles.
# 1 Guía de lectura y alcance
Este documento reúne la arquitectura y el diseño del backend discutidos después de la limpieza del proyecto. Describe el sistema que se construirá, su relación con el motor existente y una estrategia de despliegue compatible con el presupuesto de una tesis. La sección 22 documenta el flujo multicultivo ya implementado. Los contratos REST y las capas del backend descritos en las otras secciones siguen siendo el diseño de integración.
## Organización del documento

## Qué se conserva del proyecto existente
Se conserva CropSuiteLite con sus correcciones, el catálogo completo, insumos preparados, pruebas y ejecución de referencia de maíz. El backend utilizará esta base a través de una integración controlada. La documentación de arquitectura no autoriza cambios en los datos originales, en maize.inf ni en las reglas agronómicas.
La cobertura actual corresponde a Huaura. El catálogo disponible contiene 79 archivos de cultivos y variantes; el usuario puede seleccionar uno o varios. Se comprobó la ejecución conjunta de maíz, papa y arroz. La disponibilidad de los demás parámetros no implica que todos hayan sido validados agronómicamente o ejecutados en este entorno.
## Cómo interpretar los ejemplos
Los nombres en inglés, como Evaluation o ParcelSnapshot, facilitan identificar clases y contratos. El lenguaje de la interfaz puede ser español. Los ejemplos de JSON son ilustrativos y no presentan resultados calculados. Los estados, endpoints y esquemas deberán concretarse antes de generar migraciones y clientes.
Los precios se expresan en dólares estadounidenses. Son referencias consultadas durante la conversación, no una cotización ni una garantía de rendimiento. Antes de contratar se comprobarán región, disponibilidad, impuestos, IPv4, copias y límites de transferencia.
# 2 Alcance funcional y unidad de evaluación
## Huaura como cobertura de los insumos
Huaura define el ámbito para el que se han preparado datos ambientales. La unidad que enviará el usuario será una parcela, representada mediante GeoJSON. El sistema comprobará que la geometría esté dentro del ámbito admitido y que existan datos suficientes para los cálculos solicitados.
La pertenencia al límite provincial y la cobertura ambiental son condiciones diferentes. Una parcela puede estar dentro de Huaura y intersectar celdas sin suelo u otra variable necesaria. Por ello, el resultado debe informar cuánta superficie tiene datos utilizables y cómo se han tratado los faltantes.
## Flujo esperado para una persona usuaria
- Iniciar sesión y acceder a un proyecto autorizado.
- Dibujar una parcela o cargar un GeoJSON y registrar su geometría.
- Consultar la cobertura, resolución y disponibilidad de los insumos.
- Seleccionar uno o varios cultivos del catálogo, con el mismo escenario y manejo permitido.
- Solicitar una evaluación y consultar su progreso.
- Revisar aptitud, cobertura y evidencia por cultivo, junto con la comparación sobre superficie común.
- Consultar una explicación o comparar alternativas cuando estén habilitadas.
No se pedirá al usuario que calcule índices de filas y columnas de un ráster. El backend traduce la geometría a las operaciones espaciales necesarias. La entrada implementada admite Polygon o MultiPolygon en WGS84, como geometría, Feature o FeatureCollection de una sola parcela.
## Límite de resolución
La malla actual tiene 28 columnas y 21 filas, con resolución de aproximadamente 0,041666 grados. La dimensión lineal ronda los 4,6 km y varía con la dirección y la latitud. Un polígono pequeño puede quedar completamente dentro de una única celda.
Recortar esa celda a la forma de una parcela no genera una observación ambiental más detallada. El producto deberá presentar el resultado como una estimación basada en la resolución disponible. Parcelas vecinas pueden recibir valores iguales porque comparten las mismas celdas fuente.
## Dos modalidades compatibles
La consulta de resultados precalculados resume una ejecución regional compatible para una parcela. La ejecución bajo demanda calcula una combinación nueva de parámetros admitidos. El flujo actual ejecuta bajo demanda la malla ambiental regional para cada cultivo y resume únicamente la parcela solicitada. La reutilización compatible de resultados precalculados queda pendiente.
# 3 Arquitectura general del sistema
## Separación de responsabilidades
El frontend proporciona el mapa, formularios y visualización. La API valida solicitudes y aplica permisos. Los módulos del backend ejecutan casos de uso y conservan sus reglas. El worker realiza trabajos largos. La base de datos guarda información estructurada y los archivos científicos se conservan en almacenamiento persistente.
El modelo científico queda encapsulado detrás de una interfaz de aplicación. Su adaptador conoce la configuración, las rutas y el formato de los archivos de CropSuiteLite. Los controladores y los agregados del negocio no dependen de esos detalles.

Figura 1  Componentes y responsabilidades
## Arquitectura lógica y despliegue
Un bounded context define un modelo, un vocabulario y reglas coherentes. Un proceso, contenedor o servidor define dónde se ejecuta código. Estos límites pueden coincidir, pero no son equivalentes. Un worker puede ejecutar tareas del contexto de Evaluación sin convertirse por ello en otro bounded context. [1]
En la primera versión habrá una base de código del backend con módulos independientes y contratos explícitos. El worker podrá compartir paquetes de aplicación con la API, aunque arranque como proceso distinto. El motor Python puede conservar un entorno separado, especialmente si el backend se desarrolla en Java o C#.
## Criterio para separar servicios en el futuro
Se extraería un componente cuando existan motivos observables: escalado distinto, aislamiento de fallos, necesidades de recursos o evolución independiente. El tamaño de los archivos por sí solo no obliga a crear una API de GeoData. Tampoco se necesita una API HTTP propia para cada worker.
El sistema inicial no requiere Kubernetes, un servidor de GPU ni un servicio ML. Estas capacidades se evaluarían si aparecieran cargas de trabajo que las justifiquen.
# 4 Bounded contexts propuestos
Los contextos siguientes son la hipótesis inicial del modelo. Sus límites se validarán mediante casos de uso y eventos del negocio. La separación se basará en reglas y propiedad de datos, evitando convertir cada tabla o herramienta técnica en un contexto.

## Agrupaciones iniciales
Auth y users se agrupan en Identidad y acceso. Projects y parcels se agrupan en Gestión agrícola. La orquestación y la trazabilidad científica pertenecen inicialmente a Evaluación. Ranking y recommendations pueden comenzar juntos en Apoyo a decisiones.
Jobs, reports y repositories no se consideran bounded contexts por su nombre técnico. Un job implementa la ejecución de un caso de uso; un reporte puede ser una representación de resultados que pertenecen a otro contexto.
## Componentes cuyo alcance puede crecer
Un ranking que ordena puntuaciones puede ser un servicio de aplicación. Si incorpora disponibilidad de agua, costos, mercado, riesgo y preferencias, tendrá reglas propias que justifican un contexto más rico. La ampliación debe incluir fuentes y criterios comparables.
Se propuso un contexto de Experimentos por la naturaleza académica del proyecto. Inicialmente, las versiones y ejecuciones reproducibles pueden quedar en Evaluación. Experimentos se separaría si aparecen hipótesis, diseños experimentales, conjuntos de ensayos y comparaciones con ciclo de vida propio.
Organizaciones, campañas y variedades son posibilidades de evolución. No se asumirán obligatorias para el primer incremento si sus casos de uso aún no están definidos.
# 5 Propiedad de datos y colaboración entre contextos
## Cada contexto controla sus cambios
Un módulo modifica sus datos a través de sus propios casos de uso y repositorios. Los demás módulos no escriben directamente sus tablas ni acceden a sus entidades internas. Esta regla preserva las invariantes cuando cambian las implementaciones.
Se puede utilizar una única instancia de PostgreSQL. La propiedad se puede reflejar en esquemas por contexto, migraciones delimitadas y permisos técnicos cuando resulte útil. Compartir infraestructura no significa compartir libremente el modelo de dominio.
## La parcela actual y la parcela evaluada
Gestión agrícola posee la geometría vigente. Evaluación conserva un ParcelSnapshot con la versión exacta utilizada para un cálculo: identificador de parcela, versión, geometría, sistema de referencia y fecha de captura.
Si una parcela cambia de 100 a 85 hectáreas, el resultado anterior sigue asociado a la geometría de 100 hectáreas. La aplicación puede mostrar ambos, pero no debe reinterpretar silenciosamente el resultado anterior sobre el nuevo límite.
## Colaboraciones previstas

Los intercambios usan contratos públicos estables. Una consulta local mediante interfaz es suficiente cuando los módulos están en el mismo proceso. Los eventos son apropiados cuando el consumidor puede reaccionar de manera diferida, por ejemplo al finalizar una evaluación.
## Coherencia e independencia
Las transacciones protegen cambios coherentes dentro del contexto. La publicación de trabajos y la coordinación con otros procesos requiere tratar fallos y reintentos. No se mantendrá una transacción de base de datos abierta durante un cálculo de varios minutos.
Si dos contextos requieren continuamente las mismas entidades y cambios atómicos conjuntos, se revisará si la frontera propuesta es adecuada antes de añadir complejidad de coordinación.
# 6 Capas y estructura del backend
Cada bounded context contendrá sus propias capas. Domain expresa el modelo y sus reglas. Application coordina casos de uso. Infrastructure implementa persistencia e integraciones. Interfaces expone REST u otros mecanismos de entrada.
backend/
modules/
evaluation/
Domain/
Model/
Aggregates/
Entities/
ValueObjects/
Events/
Repositories/
IEvaluationRepository
Services/
Application/
Commands/
Queries/
Services/
IEvaluationCommandService
EvaluationCommandService
IEvaluationQueryService
EvaluationQueryService
Ports/
ICropSuitabilityEngine
IEnvironmentalDataProvider
Infrastructure/
Repositories/
CropSuite/
Messaging/
ACL/
Interfaces/
REST/
Resources/
Transform/
EvaluationController

## Convención de commands y queries
La estructura planteada por el usuario ubicaba Commands, Queries y las interfaces de command/query services en Domain. La recomendación posterior fue situarlos en Application porque representan casos de uso. Esta será la estructura de referencia del documento. Si la convención académica exige la ubicación original, se puede conservar sin permitir dependencias de Domain hacia HTTP, ORM o servicios externos. [2]
El nombre de una carpeta no reemplaza la dirección de las dependencias. Las implementaciones de infraestructura satisfacen interfaces internas y se conectan al iniciar la aplicación mediante configuración o inyección de dependencias.
# 7 Modelo de dominio y repositorios
## Agregados y entidades
Un agregado es un conjunto de objetos con una raíz que protege reglas de consistencia. Evaluation es un candidato a raíz para controlar la solicitud y sus transiciones. Parcel es un candidato dentro de Gestión agrícola. Sus fronteras concretas deben ajustarse a qué cambios necesitan ser atómicos.
Las entidades tienen identidad y continuidad en el tiempo. Una versión de parcela, una ejecución o un resultado pueden modelarse como entidades si su ciclo de vida lo requiere. No toda tabla necesita convertirse en un agregado separado.
## Value objects y mensajes
Los value objects representan valores con significado, validación e igualdad por contenido. Ejemplos: ParcelId, DatasetVersion, SuitabilityScore o AnalysisConfiguration. Deben ser inmutables cuando sea posible. Un enum sirve para opciones cerradas, como el tipo de manejo, si el catálogo realmente es fijo.
Commands y queries se expresan como mensajes inmutables. Los records son una opción en lenguajes que los ofrecen. En Python se usaría un equivalente adecuado. La selección de Java, C# o Python para el backend aún no está cerrada y no cambia estos conceptos.
## Reglas candidatas

## Repositorios y servicios de dominio
IEvaluationRepository pertenece al dominio y define la persistencia del agregado. EvaluationRepository se implementa en Infrastructure/Repositories. Se proponen repositorios por agregado, no automáticamente por tabla. [3]
Una consulta de listado puede usar una proyección o modelo de lectura, sin reconstruir un agregado completo. Esa proyección no debe convertirse en una vía para modificar reglas del negocio.
Los servicios de dominio se reservan para reglas que no encajan naturalmente en una entidad o agregado. Programar un job, enviar una solicitud HTTP o traducir un archivo de CropSuiteLite es coordinación o infraestructura, no una regla de dominio.
# 8 Application y separación de comandos y consultas
## Servicios de aplicación
EvaluationCommandService coordina acciones que cambian el estado del sistema. Carga el agregado mediante su contrato de repositorio, invoca sus operaciones, persiste los cambios y solicita la ejecución cuando corresponde. Las reglas de consistencia permanecen en el dominio.
EvaluationQueryService obtiene información para responder consultas: estado de una evaluación, resultados disponibles o evidencia. Se puede adoptar esta separación de responsabilidades sin utilizar bases de datos distintas ni una plataforma compleja de CQRS.
## Contratos ilustrativos

La cancelación es una capacidad propuesta; requiere soporte del worker y no debe declararse instantánea si el proceso científico aún continúa.
## Ejemplo de coordinación
- Comprobar identidad, acceso al proyecto y formato del comando.
- Obtener la versión autorizada de la parcela mediante el contrato público de Gestión agrícola.
- Consultar compatibilidad y cobertura de los insumos en Información geoambiental.
- Crear la evaluación con su snapshot y referencias inmutables.
- Persistir la solicitud y programar el trabajo de forma recuperable.
- Devolver un identificador para consultar el progreso.
## Puertos para dependencias externas
ICropSuitabilityEngine representa la capacidad de ejecutar el cálculo. IEnvironmentalDataProvider representa la obtención de datos compatibles. Un puerto de almacenamiento puede guardar y recuperar artefactos. Los puertos se definen donde se necesitan; en estos casos, Application es una ubicación apropiada.
La aplicación no debería construir comandos de consola a partir de texto arbitrario del usuario. El adaptador traduce opciones verificadas a la configuración admitida del motor.
# 9 Interfaces REST y transformación de recursos
## Responsabilidad de la interfaz
El controller recibe HTTP, interpreta el recurso, delega el caso de uso y transforma el resultado en una respuesta. Resources contiene los DTO de entrada y salida. Transform convierte esos DTO en commands o queries y transforma los resultados de aplicación en recursos públicos.
Los DTO públicos no exponen directamente entidades del ORM ni agregados completos. Esto permite cambiar la persistencia y el dominio sin obligar a modificar cada consumidor. Las validaciones de estructura pertenecen a la entrada; las reglas del negocio se aplican también dentro del sistema.
CreateEvaluationResource
-> RequestEvaluationCommand
-> EvaluationCommandService
-> Resultado de aplicación
-> EvaluationResource

## API propuesta para el primer incremento

Estas rutas son una propuesta de diseño. La cobertura dependerá de las capas y del escenario; sus parámetros deben quedar explícitos en el contrato. La aceptación de una evaluación asíncrona puede responder 202 con su identificador y ubicación de consulta.
## Contrato de la solicitud
{
"parcelId": "parcela-ejemplo",
"parcelVersion": 1,
"crops": ["maize", "potato", "rice"],
"scenarioId": "access-ssp126-2021-2040",
"management": "rainfed"
}

El servidor resuelve ese identificador de escenario a versiones exactas. La lista de cultivos será obligatoria, sin duplicados y con identificadores del catálogo. Cada resultado incluirá cropId y estado; la comparación informará alternativas fallidas o sin cobertura. El servidor rechazará solicitudes no autorizadas antes de calcular.
# 10 ACL e integración entre bounded contexts
## Objetivo de la capa anticorrupción
La ACL traduce el contrato de otro contexto al modelo del consumidor. Evita que conceptos externos, formatos o decisiones de persistencia se propaguen por el dominio propio. No es un mecanismo de autenticación; los permisos siguen siendo necesarios. [4]
En Evaluación, IEnvironmentalDataProvider expresa la información que necesita el caso de uso. EnvironmentalDataAdapter, ubicado en Infrastructure/ACL, consulta el contrato público de Información geoambiental y convierte la respuesta al modelo esperado.
## Ejemplo de intercambio
Información geoambiental puede publicar una descripción de DatasetVersion con cobertura, unidad, formato y referencia de almacenamiento. Evaluación la convierte en un EnvironmentalInputManifest con los insumos concretos requeridos por una ejecución. No recibe una entidad del ORM ni consulta directamente la tabla del proveedor.
Gestión agrícola puede publicar una ParcelDescription. Evaluación construye su ParcelSnapshot y conserva la versión usada. Los cambios futuros del modelo interno de parcelas se absorben en la traducción.
## Cómo exponer y consumir contratos
El proveedor puede ofrecer una fachada pública bajo Interfaces/ACL o un paquete Contracts. El consumidor utiliza su propio puerto y adaptador. El nombre exacto de estas carpetas es una convención; se debe mantener clara la propiedad de cada contrato.
En un monolito, la fachada puede invocarse mediante una llamada local. Si el proveedor se extrae a un servicio, el adaptador puede pasar a usar HTTP o mensajería. Los casos de uso del consumidor deberían conservar la misma intención.
## Eventos y resultados finalizados
Un evento EvaluationCompleted puede avisar a Apoyo a decisiones de que existen resultados. El evento debería incluir identificadores y versiones, evitando transportar todos los rásteres. El consumidor recupera la evidencia necesaria mediante el contrato autorizado.
Los eventos de integración pueden necesitar un contrato distinto al evento interno del dominio. Deben considerarse duplicados y reintentos, por lo que las reacciones tendrán que ser idempotentes.
## Cuándo simplificar
Una ACL es útil cuando hay traducción de modelos. Si dos componentes ya comparten un contrato pequeño y estable, no hace falta añadir una cadena de transformaciones idénticas. Lo que siempre se conserva es la frontera: otro contexto no accede a entidades o repositorios internos.
# 11 Integración de CropSuiteLite
## Motor científico detrás de un adaptador
CropSuiteLite ejecuta el modelo de aptitud; el backend administra su uso. CropSuiteAdapter traduce una solicitud verificada a archivos de configuración, organiza las entradas, invoca el motor y devuelve referencias a resultados comprobados. La API no contiene lógica interna del motor.
La base implementada es src.multicrop.run_evaluation, invocable desde Python o mediante evaluate.py. Ejecuta un subproceso aislado por cultivo. El futuro adaptador del backend podrá llamar a esta capacidad desde el worker; las capas y la cola aún no están implementadas.
## Secuencia del worker
- Recuperar la evaluación y verificar que puede comenzar.
- Crear un directorio de trabajo propio para la ejecución.
- Resolver versiones exactas de datos, parámetros y motor.
- Preparar una carpeta aislada y una copia exacta de parámetros por cultivo seleccionado.
- Ejecutar los cultivos por turnos, con límites de procesos internos y fallos independientes.
- Verificar archivos, dimensiones, unidades, máscaras y valores esperados.
- Resumir la parcela, comparar sobre cobertura común y publicar estados y artefactos por cultivo.
Las entradas compartidas deben tratarse como inmutables. Cada ejecución tiene rutas propias para impedir colisiones entre archivos INI, temporales y resultados. No se reutilizará un directorio global de salida para solicitudes distintas.
## Identidad de la ejecución y reutilización
Una clave de reutilización debe incluir la versión del motor, parámetros del cultivo, insumos, escenario, manejo y opciones científicas. La geometría o ámbito de cálculo y el método de agregación también forman parte de la identidad cuando afectan al resultado.
Es útil distinguir ScientificRun, que representa el cálculo sobre una malla, y ParcelAssessment, que representa el resumen para una geometría. Varias parcelas podrían reutilizar el mismo ScientificRun si sus condiciones son compatibles.
La existencia de un archivo no demuestra compatibilidad. El backend comparará el manifiesto antes de reutilizar una ejecución. La ruta operativa actual reutiliza archivos existentes, por lo que una medición de rendimiento debe forzar una ejecución aislada sin caché.
## Límite de las correcciones existentes
La interpolación, las unidades y las máscaras del pipeline deben conservarse. El backend no alterará maize.inf para producir una puntuación mayor. Una aptitud baja válida es un resultado posible y debe explicarse con los factores realmente obtenidos.
# 12 Ejecución asíncrona y control de recursos
## Solicitud y trabajo científico
La API registra la evaluación y devuelve una referencia. Una cola entrega el trabajo al worker, que actualiza el estado. El navegador consulta el progreso mediante polling; otros mecanismos de notificación pueden añadirse después.
Celery con un broker compatible, como Redis según la versión elegida, es la propuesta inicial del entorno Python. API, cola y worker pueden vivir en el mismo VPS. Los resultados durables pertenecen a la base de datos y al almacenamiento de artefactos, no exclusivamente al broker.
## Estados propuestos

El manifiesto actual usa running, completed, partial y failed para la solicitud; por cultivo usa running, succeeded, no_coverage y failed. Un fallo no impide procesar los restantes. La futura API mapeará estos estados y conservará la distinción entre ausencia de datos y fallo.
## Reintentos y entrega confiable
Las tareas pueden repetirse por fallos de red o reinicios. Se necesita idempotencia para impedir resultados duplicados y sobrescrituras incoherentes. Los fallos temporales admiten reintentos limitados; una geometría inválida o la ausencia de insumos requiere corregir la solicitud.
La persistencia de una evaluación y su envío a la cola deben ser recuperables. Un patrón outbox o un mecanismo equivalente puede impedir que una solicitud quede registrada pero nunca programada. Es una propuesta de implementación, no una capacidad actual del repositorio.
## Concurrencia inicial
Se comenzará con una evaluación pesada a la vez. CropSuiteLite ya puede crear procesos internos; lanzar muchos workers multiplica el uso de CPU y memoria. La concurrencia del motor y de la cola se ajustará conjuntamente con mediciones. [5]
La preparación ambiental compartida solo se reutilizará cuando sea inmutable y compatible. El progreso mostrará fases comprobables; no se inventará un porcentaje exacto si el motor no lo proporciona.
# 13 Datos geoambientales y evaluación espacial
## Catálogo de insumos
Información geoambiental conservará para cada capa su fuente, variable, versión, unidad, CRS, resolución, extensión, máscara de datos válidos, período temporal, escenario, checksum y ubicación. Estas propiedades permiten comprobar compatibilidad antes de ejecutar.
El almacenamiento puede comenzar en el disco persistente del VPS. El catálogo debe usar referencias que puedan migrar a almacenamiento de objetos sin modificar el modelo de dominio. Los datos originales de descarga pueden conservarse en un repositorio de respaldo sin estar presentes en el servidor público.
## Preparación de una parcela
Se validará que el GeoJSON tenga geometría admitida y coordenadas interpretables. Se comprobarán topología, pertenencia al proyecto, ubicación en Huaura y tamaño razonable de la solicitud. El GeoJSON público utilizará longitud y latitud conforme al contrato definido; los cálculos de superficie usarán un procedimiento geodésico o una proyección apropiada.
Para ejecutar el motor puede ser necesaria una ventana con margen alrededor de la parcela. Operaciones como pendiente o interpolación pueden requerir vecindad. Recortar prematuramente al límite exacto del polígono puede modificar los resultados de borde.
## Resumen de aptitud
El resumen implementado pondera cada celda válida por el área de su intersección con la parcela, calculada en EPSG:6933. Devuelve media, mínimo, máximo, celdas válidas, superficie cubierta y superficie de aptitud cero para cultivo, clima y suelo. La comparación usa únicamente la superficie válida común de aptitud de cultivo.
Cobertura válida = área con datos utilizables / área de la parcela

Media ponderada = suma de aptitud por área intersectada válida
/ suma de áreas intersectadas válidas

La media describe la parcela según ese criterio; no reemplaza la regla con la que CropSuiteLite combina los factores dentro de cada celda. Incorporar clases, umbrales de cobertura o una medida conservadora requiere una decisión funcional y científica explícita.
## Tratamiento de los faltantes
Una aptitud 0 es una evaluación válida de baja aptitud. Nodata significa que no puede obtenerse el resultado con la información disponible. No se asignará cero a las áreas faltantes ni se ocultarán mediante una media sin cobertura.
En las comprobaciones existentes se identificaron 231 celdas terrestres con clima completo y siete celdas sin resultado de cultivo por faltantes en los suelos originales. Estos datos describen la cobertura actual y no sustituyen una comprobación específica del polígono solicitado.
# 14 Persistencia y trazabilidad científica
## Base de datos y archivos
PostgreSQL con PostGIS almacenará usuarios referenciados, proyectos, geometrías, solicitudes, metadatos y resultados estructurados. Los rásteres y NetCDF se guardarán como archivos en almacenamiento persistente. La base de datos registra su identificador, ubicación, formato y checksum.
Esto es una decisión práctica para la primera versión, no una imposibilidad técnica de guardar rásteres en PostgreSQL. La separación facilita conservar y servir los artefactos sin agrandar innecesariamente las tablas transaccionales.
## Registros propuestos

Los nombres son candidatos; las tablas y relaciones finales derivarán de los agregados y consultas. Los archivos pueden compartirse entre resultados compatibles sin duplicar su contenido, manteniendo referencias inequívocas.
## Manifiesto reproducible
Una ejecución conservará la versión o commit del motor, versiones de dependencias relevantes, copia o hash de los parámetros del cultivo, configuración efectiva e insumos identificados. También registrará el escenario, manejo, ámbito espacial, transformaciones, tiempo y estado final.
El resumen de parcela añadirá la geometría versionada, el método espacial, la escala de puntuación y los porcentajes de cobertura. Cuando una operación incluya aleatoriedad, se registrará la semilla u otra condición necesaria para reproducirla.
## Auditoría y evidencia
La auditoría responde quién hizo qué y cuándo. La evidencia científica explica con qué datos y reglas se obtuvo una estimación. Un log de servidor no reemplaza ninguna de las dos. Los mensajes de fallo pueden enlazar detalles técnicos de acceso restringido sin exponer rutas internas al usuario.
# 15 Ranking recomendaciones y explicaciones con LLM
## Comparaciones compatibles
La comparación implementada ordena la aptitud de los cultivos seleccionados sobre la intersección de sus celdas válidas en la misma parcela. Usa medias ponderadas por superficie y conserva empates. Publica la cobertura común y excluye alternativas sin datos o fallidas; si no hay superficie común, no genera ranking. La política de cobertura mínima para recomendaciones queda pendiente.
La aptitud agrícola no equivale a rentabilidad. Incorporar precio, mercado, disponibilidad real de agua o preferencias requiere fuentes adicionales y criterios explícitos. Esas reglas pertenecen a Apoyo a decisiones y no deben modificar silenciosamente el resultado científico.
## Evidencia que recibe la explicación
La capa LLM consumirá evidencia estructurada y autorizada. Debería recibir la puntuación, escala, factores limitantes, variables con sus unidades, período considerado, cobertura y referencias de procedencia. Los campos ausentes deben permanecer identificados como tales.
Se usará un nombre como SuitabilityEvidence o CalculationEvidence para el registro verificable. El término reasoning_trace de la propuesta inicial no implica almacenar un razonamiento privado del modelo; lo necesario es conservar entradas, reglas, factores y fuentes comprobables.
## Límites de la explicación
Una puntuación baja de precipitación no basta para afirmar que hubo déficit durante la fase reproductiva. Esa afirmación requiere evidencia temporal que identifique la fase. Tampoco puede recomendarse una variedad o garantizarse una mejora por riego si la evidencia disponible no respalda esa conclusión.
El LLM explica el resultado, pero no recalcula ni reemplaza la puntuación de CropSuiteLite. Darle evidencia reduce incertidumbre, aunque no elimina la posibilidad de respuestas incorrectas. Se aplicarán validaciones de salida y se facilitará consultar los factores originales.
## Riego y escenarios alternativos
Evaluar riego como alternativa requiere una configuración explícita y compatible, además de reconocer que la aptitud modelada no demuestra disponibilidad física de agua. Una comparación de manejo conserva dos ejecuciones identificables y sus diferencias.
## Costos y disponibilidad
La explicación puede empezar con plantillas deterministas y añadir un LLM cuando su caso de uso esté definido. Se establecerán cuotas por usuario, límites de longitud y un presupuesto aplicado por el backend. Si la API externa falla o se agota el presupuesto, el resultado científico seguirá consultable.
RAG se incorporaría si hay un corpus agronómico autorizado y una necesidad concreta de recuperar fuentes. No es un requisito para explicar los factores estructurados de una evaluación.
# 16 Despliegue público con presupuesto pequeño
## Distribución inicial propuesta
El frontend puede publicarse en Vercel. Un VPS ejecutará el backend modular, la cola y el worker en procesos o contenedores separados. Supabase puede proporcionar PostgreSQL, PostGIS y autenticación. Los archivos operativos caben inicialmente en el disco persistente del servidor.

Figura 2  Distribución inicial de despliegue
## Operación del servidor
La API atenderá solicitudes cortas y el worker ejecutará tareas de fondo. El motor contará con un entorno Python reproducible. Los secretos se configurarán fuera del repositorio. La base de datos y la cola no se expondrán públicamente sin necesidad.
Se configurarán HTTPS, reinicio de procesos, logs, límites de recursos y copias de los datos persistentes. Se verificará que los servicios se recuperen tras reiniciar el VPS. Estas tareas de operación son parte del costo de trabajo, aunque el alquiler sea económico.
El frontend estático de Vercel no ejecutará CropSuiteLite. La llamada del navegador termina en la API, que devuelve una referencia de evaluación. Las actualizaciones de estado se consultan sin mantener abierta la solicitud durante todo el cálculo.
## Opciones tecnológicas sin cerrar
FastAPI fue propuesto por afinidad con el motor Python; no se ha elegido definitivamente el lenguaje del backend. Si los requisitos académicos favorecen Java o C#, las capas y contratos se mantienen, y el worker sigue ejecutando CropSuiteLite en Python.
No es necesario contratar Redis, GeoData y CropSuite como servicios independientes. Su separación lógica puede conservarse dentro de un solo servidor. La extracción posterior requerirá medir necesidades reales y mantener contratos estables.
# 17 Presupuesto y alternativas de alojamiento
## Presupuesto inicial orientativo

El total es una reserva de planificación, no la suma de una cotización cerrada. Dominio propio, impuestos, IPv4, copias adicionales, transferencia y servicios de mapas pueden añadir cargos. Un subdominio del proveedor permite posponer la compra de un dominio cuando cubre las necesidades de acceso.
Vercel Hobby se limita al uso personal no comercial. Supabase Free incluye 500 MB de base de datos y 1 GB de archivos, puede pausarse después de una semana de inactividad y no incluye las mismas garantías de un plan de pago. PostGIS está disponible como extensión. [6][7][8]
Como referencia, Hetzner publica el CX33 de 4 vCPU y 8 GB de RAM a US$9,99 mensuales en Alemania/Finlandia, sin impuestos ni IPv4 en esa tarifa. Es un candidato para medir; no se ha demostrado aún que satisfaga la carga esperada. No se debe asumir que US$5 a US$10 compran 16 GB de RAM. [9][10]
## Alternativa prácticamente gratuita
Una primera web puede consultar resultados precalculados y resumirlos por parcela. Render ofrece servicios web gratuitos, pero se suspenden después de 15 minutos sin tráfico, usan disco efímero y no incluyen workers gratuitos. Sus bases PostgreSQL gratuitas expiran a los 30 días; no se proponen para guardar permanentemente la aplicación. [11]
Un worker en la computadora personal permite una demostración supervisada. Cuando la computadora se apaga, los nuevos cálculos no se ejecutan. Para acceso público independiente se prefiere el VPS.
Los insumos preparados y la salida de referencia ocupaban aproximadamente 9,5 MiB en la revisión inicial, excluyendo descargas originales y entorno. Cada solicitud multicultivo añade salidas y clima derivado por cultivo; deben medirse ese crecimiento y su retención. Cloudflare R2 queda como alternativa si crecen los artefactos; sus cuotas y cargos deben verificarse. [12]
# 18 Calidad seguridad y validación antes de publicar
## Pruebas del backend
Las pruebas de dominio cubrirán invariantes y transiciones. Las de aplicación verificarán permisos, coordinación, versionado e idempotencia. Las de integración comprobarán persistencia, contratos entre contextos y lectura de artefactos. Las de extremo a extremo recorrerán una parcela hasta su resultado.
Se conservarán las pruebas existentes de CropSuiteLite. Las 22 pruebas superadas cubren el pipeline y el flujo multicultivo, incluidos selección, geometrías, nodata, pesos espaciales, comparación y fallos parciales. Además, se ejecutaron maíz, papa y arroz con el motor real, tanto sobre el límite provincial como sobre una parcela sintética pequeña. Esto verifica la integración técnica; no equivale a validación agronómica ni a un despliegue web.
## Casos espaciales necesarios

## Seguridad aplicable al uso público
La autorización debe comprobarse en cada operación sobre proyectos, parcelas y resultados. El backend no confiará en que el frontend oculte identificadores ajenos. Las claves privilegiadas de almacenamiento y base de datos no se enviarán al navegador.
Se limitarán tamaño y complejidad del GeoJSON, frecuencia de solicitudes y número de evaluaciones simultáneas por usuario. Las referencias de archivos las resolverá el servidor; no se aceptarán rutas arbitrarias para ejecutar el motor. Se registrarán acciones relevantes sin guardar secretos ni contenido innecesario.
## Medición de capacidad y recuperación
Antes de contratar definitivamente se medirá tiempo, memoria máxima, CPU y tamaño de salidas con una ejecución completa sin caché. Después se probará la concurrencia limitada en el servidor elegido, junto a API y cola.
Una copia de seguridad debe comprobarse restaurando una muestra. La publicación incluirá un ensayo de reinicio del worker y recuperación de una tarea interrumpida. Los resultados finalizados deben continuar consultables aunque el servicio LLM no esté disponible.
# 19 Secuencia de implementación y decisiones pendientes
## Incrementos propuestos

## Casos de uso para validar el modelo
Se propone una sesión de modelado con registro de parcela, verificación de cobertura, solicitud de evaluación, consulta de factores y comparación de configuraciones. Cambiar el escenario climático o el manejo puede incorporarse cuando existan insumos y parámetros admitidos.
El objetivo es identificar eventos, comandos, reglas y responsables. No se requiere un contexto de Experimentos solo para registrar hashes; se considerará si los casos de uso científicos necesitan una organización adicional.
## Decisiones por cerrar antes de implementar contratos definitivos
Se debe elegir lenguaje y framework del backend, y confirmar si la convención académica exige commands y queries dentro de Domain. El resumen actual usa intersecciones por área y admite Polygon y MultiPolygon; el catálogo ofrece 79 parámetros. Quedan por definir la cobertura mínima para recomendar, los escenarios públicos y la validación de los cultivos restantes.
El despliegue requiere confirmar presupuesto máximo, duración de la publicación y uso esperado. Se debe medir capacidad antes de fijar cantidad de workers. Las tarifas del LLM y del mapa dependen de los proveedores y del volumen; aún no se ha contratado ninguno.
El flujo CLI y el servicio Python multicultivo están implementados. La estructura modular del backend, autenticación, persistencia, cola y publicación continúan pendientes; no se han contratado servicios.
# 20 Registro de decisiones y glosario
## Decisiones de arquitectura

## Glosario
Bounded context. Frontera donde un modelo y su lenguaje tienen significado coherente. No equivale automáticamente a un servidor.
Agregado. Conjunto de objetos cuya raíz controla reglas de consistencia y operaciones admitidas.
Command y query. Mensajes que expresan respectivamente una intención de cambio y una solicitud de lectura.
Puerto y adaptador. Contrato de una capacidad requerida e implementación que conecta con una tecnología o sistema concreto.
ACL. Capa anticorrupción que traduce un modelo externo al del contexto consumidor.
DTO o resource. Representación de datos para una interfaz; no contiene necesariamente el modelo completo del dominio.
Worker. Proceso que ejecuta trabajos en segundo plano y publica su resultado o estado.
Idempotencia. Propiedad que permite repetir una operación sin duplicar indebidamente sus efectos.
Snapshot y manifiesto. Copia versionada del estado utilizado y registro de las entradas y condiciones de ejecución.
Nodata. Ausencia de información utilizable. No equivale a una aptitud científica igual a cero.
# 21 Fuentes y referencias
Las fuentes técnicas respaldan los conceptos de modelado y las condiciones de los servicios. Las decisiones específicas de arquitectura corresponden al diseño del proyecto. Las referencias de proveedores se consultaron durante la conversación del 10 de septiembre de 2026; deben revisarse antes de contratar.
1. Martin Fowler. Bounded Context. Definición de fronteras del modelo y relaciones entre contextos. Consultar fuente
2. Microsoft. Implement the microservice application layer using the Web API. Comandos, coordinación y modelo de dominio. Consultar fuente
3. Microsoft. Design the infrastructure persistence layer. Contratos e implementaciones de repositorios. Consultar fuente
4. Microsoft. Anti-Corruption Layer pattern. Traducción entre modelos de subsistemas. Consultar fuente
5. Celery. Optimizing. Ajustes según carga, recursos y concurrencia. Consultar fuente
6. Vercel. Hobby Plan. Condiciones y límites del plan gratuito. Consultar fuente
7. Supabase. Pricing. Cuotas de base de datos, archivos y condiciones de Free. Consultar fuente
8. Supabase. PostGIS Geo queries. Disponibilidad de la extensión espacial. Consultar fuente
9. Hetzner. Price Adjustment 15 June 2026. Tarifas por región y exclusiones. Consultar fuente
10. Hetzner. Gaming Server. Referencia de especificaciones de CX33. Consultar fuente
11. Render. Deploy for Free. Suspensión, persistencia y tipos de servicio gratuitos. Consultar fuente
12. Cloudflare. R2 Pricing. Almacenamiento, operaciones y cuotas gratuitas. Consultar fuente
## Evidencia del proyecto
La cobertura y el estado del motor pueden consultarse en README.md, CropSuiteLite/docs/huaura_environment_correction.md y el report.json de results/huaura_environment_validation/run_mw_8gsjo. El tamaño de los insumos y las salidas es una medición local de las carpetas operativas. La implementación multicultivo se documenta en CropSuiteLite/docs/multicrop_evaluation.md y tests/test_multicrop.py. Los manifiestos evaluation.json conservan la evidencia de las ejecuciones. La arquitectura web corresponde al desarrollo siguiente.
# 22 Uso de la evaluación multicultivo implementada
## Una solicitud para la misma parcela
evaluate.py recibe el GeoJSON y los identificadores seleccionados entre 79 parámetros disponibles. Valida que la geometría esté completamente dentro de Huaura, conserva una copia y ejecuta los cultivos por turnos. “Una evaluación multicultivo” significa una solicitud compartida con resultados independientes; no exige ejecutar todos los cálculos simultáneamente.
Desde la carpeta CropSuiteLite, consultar el catálogo y evaluar una parcela:
.venv/Scripts/python.exe evaluate.py --list-crops
.venv/Scripts/python.exe evaluate.py --parcel mi_parcela.geojson --crops maize potato rice

El archivo tests/fixtures/huaura_parcel_example.geojson permite probar el flujo con un polígono sintético; no representa una propiedad agrícola registrada. La opción --whole-huaura está reservada a la comprobación regional explícita. El lanzador anterior conserva la ejecución de referencia de maíz.
## Archivos y comparación
Cada solicitud crea results/evaluations/evaluation_*/ con parcel.geojson y evaluation.json. Cada subcarpeta de cultivo contiene su configuración, parámetros originales copiados, log, salidas completas y una carpeta parcel con rásteres de aptitud de cultivo, clima y suelo.
El manifiesto registra estados, hashes de entradas y código, tiempos, superficie válida, cobertura y puntuaciones en escala de 0 a 100. La media se pondera por el área de intersección entre cada celda y la parcela en EPSG:6933. El ranking recalcula esa media sobre la superficie válida común a los cultivos comparables. Nodata se excluye; cero sigue siendo una aptitud válida.
La parcela pequeña de prueba obtuvo resultados completos para maíz, papa y arroz. El caso provincial también completó los tres cultivos. Las pruebas automáticas verifican además que una alternativa fallida no interrumpa las restantes y que se informe un estado parcial.
## Alcance y trabajo siguiente
El motor calcula todavía la malla ambiental regional por cultivo y después delimita el resumen. Los rásteres de parcela conservan las celdas que la intersectan, incluida la parte exterior de las celdas de borde; el resumen usa solo el área interior. No se crean observaciones más finas que la malla original.
Cada cultivo vuelve a preparar el clima y conserva sus derivados; el tiempo y el almacenamiento crecen con la selección. No hay todavía caché compartida, cola persistente, reanudación automática, API REST ni interfaz web. El backend futuro deberá añadir permisos, cuotas y recuperación de tareas, y consumir este servicio desde su adaptador de infraestructura.
| Categoría | Situación |
| --- | --- |
| Dirección acordada | Monolito modular, contextos de negocio, separación por capas y motor desacoplado. |
| Base técnica existente | Motor corregido, catálogo de 79 parámetros y evaluación multicultivo por GeoJSON mediante CLI y servicio Python. |
| Funcionalidad pendiente | Backend web por contextos, interfaz de selección, usuarios, persistencia, cola y despliegue público. |
| Diseño de referencia | Contratos, nombres de clases, estados, endpoints y tablas de este documento orientan la implementación. |
| Decisiones aún abiertas | Lenguaje del backend, límites de contextos, cobertura mínima y capacidad del servidor. |
| Secciones | Contenido |
| --- | --- |
| 2 y 3 | Problema que resuelve la aplicación y arquitectura general. |
| 4 y 5 | Bounded contexts, propiedad de los datos y reglas de colaboración. |
| 6 a 9 | Capas, modelo de dominio, servicios, commands, queries y API REST. |
| 10 a 13 | ACL, integración con CropSuiteLite, ejecución asíncrona y procesamiento espacial. |
| 14 y 15 | Persistencia, evidencia científica, recomendaciones y LLM. |
| 16 y 17 | Despliegue público, presupuesto y alternativas gratuitas. |
| 18 y 19 | Calidad, seguridad, secuencia de implementación y decisiones pendientes. |
| 20 y 21 | Registro de decisiones, glosario y fuentes. |
| 22 | Uso del flujo multicultivo implementado y alcance verificado. |
| Contexto | Responsabilidad principal | Modelo que controla |
| --- | --- | --- |
| Identidad y acceso | Identificar usuarios y administrar roles y permisos. | Usuario, membresía y permisos de acceso. |
| Gestión agrícola | Gestionar proyectos y parcelas y conservar sus versiones. | Proyecto, parcela y versiones de geometría. |
| Información geoambiental | Describir los insumos y determinar su cobertura y calidad. | Dataset, versión, capa y descripción de cobertura. |
| Evaluación agroclimática | Gestionar solicitudes, ejecución, resultados y evidencia. | Evaluación, ejecución y resultado científico. |
| Apoyo a decisiones | Comparar alternativas y producir recomendaciones fundamentadas. | Criterios, comparación y explicación. |
| Consumidor | Proveedor | Información intercambiada |
| --- | --- | --- |
| Gestión agrícola | Identidad y acceso | Identidad y autorización necesarias para operar sobre el proyecto. |
| Evaluación | Gestión agrícola | Descripción pública y versión de la parcela autorizada. |
| Evaluación | Información geoambiental | Versiones de insumos, cobertura y referencias de archivos compatibles. |
| Apoyo a decisiones | Evaluación | Resultados finalizados, factores, cobertura y evidencia. |
| Objeto | Regla que debe proteger |
| --- | --- |
| Parcela | Cada cambio de geometría genera una versión identificable. |
| Evaluación | Conserva parcela, configuración y lista única de cultivos; reúne sus estados y resultados. |
| Ejecución | No puede declararse exitosa sin verificar los artefactos esperados. |
| Resultado | Distingue falta de datos de una aptitud válida igual a cero. |
| Puntuación | Expresa su escala y no se mezcla con porcentajes de cobertura. |
| Mensaje | Intención | Resultado esperado |
| --- | --- | --- |
| CreateParcelCommand | Registrar una parcela autorizada. | Identificador y versión inicial. |
| RequestEvaluationCommand | Solicitar una parcela con una lista de cultivos y configuración admitida. | Identificador y estado inicial. |
| CancelEvaluationCommand | Solicitar la cancelación si el estado lo permite. | Estado de la solicitud de cancelación. |
| GetEvaluationQuery | Consultar progreso y metadatos. | Modelo de lectura de la evaluación. |
| GetEvaluationResultQuery | Obtener resultados y cobertura. | Resultado consultable o estado pendiente. |
| GetSuitabilityEvidenceQuery | Consultar evidencia y procedencia. | Descripción trazable de factores e insumos. |
| Método y ruta | Uso |
| --- | --- |
| POST /api/v1/projects | Registrar un proyecto. |
| POST /api/v1/projects/{id}/parcels | Registrar una parcela del proyecto. |
| GET /api/v1/parcels/{id}/coverage | Consultar cobertura para una configuración indicada. |
| GET /api/v1/crops | Consultar cultivos y variantes disponibles. |
| POST /api/v1/evaluations | Solicitar una evaluación para varios cultivos. |
| GET /api/v1/evaluations/{id} | Consultar estado y progreso disponible. |
| GET /api/v1/evaluations/{id}/result | Obtener resultado y resumen espacial. |
| GET /api/v1/evaluations/{id}/evidence | Consultar factores, versiones y procedencia. |
| Estado | Significado |
| --- | --- |
| Queued | Solicitud aceptada y pendiente de ejecución. |
| Preparing | Resolución de insumos y preparación del trabajo. |
| Running | Motor científico en ejecución. |
| Summarizing | Verificación y resumen espacial de las salidas. |
| Succeeded | Resultado publicado con artefactos comprobados. |
| Failed | Ejecución fallida con causa identificada. |
| Cancelled | Cancelación completada y recursos liberados. |
| Registro | Información esencial |
| --- | --- |
| Parcel y ParcelVersion | Proyecto, geometría, versión y metadatos de superficie. |
| DatasetVersion | Fuente, variable, unidad, cobertura, período y hash. |
| Evaluation | Solicitante, snapshot, configuración y estado. |
| ScientificRun | Motor, parámetros, manifiesto, intentos y tiempos. |
| EvaluationResult | Cultivo, resumen, cobertura y método de agregación. |
| SuitabilityEvidence | Factores, valores, unidades y procedencia. |
| Artifact | Tipo, ubicación, tamaño, checksum y ejecución propietaria. |
| AuditEntry | Actor, acción, recurso afectado y fecha. |
| Componente | Propuesta | Estimación mensual |
| --- | --- | --- |
| Frontend | Vercel Hobby para uso admitido por el plan. | US$0 |
| API y worker | Un VPS para backend, cola y cálculo. | US$10 a US$15 |
| Base de datos y autenticación | Supabase Free dentro de cuotas. | US$0 |
| Archivos operativos | Disco persistente del VPS y copia externa. | Incluido al inicio; revisar respaldo. |
| LLM opcional | API con presupuesto propio. | Reserva de US$0 a US$5 |
| Total de planificación | Aplicación pública pequeña. | Aproximadamente US$15 a US$20 |
| Caso | Comportamiento a comprobar |
| --- | --- |
| Parcela fuera de Huaura | Rechazo o respuesta de cobertura no admitida, según contrato. |
| Parcela pequeña dentro de una celda | Resultado coherente con la resolución y sin detalle artificial. |
| Parcela con nodata parcial | Cobertura explícita y resumen solo de valores válidos. |
| Parcela sin cobertura útil | Resultado de información insuficiente, no aptitud cero. |
| Edición posterior de la parcela | Resultado anterior ligado a su versión original. |
| Solicitud repetida o reintento | Reutilización o ejecución idempotente según corresponda. |
| Etapa | Entregable | Criterio para avanzar |
| --- | --- | --- |
| 1 Modelado | Casos de uso, eventos, vocabulario y contextos revisados. | Propiedad de datos y responsabilidades entendidas. |
| 2 Base modular | Capas, contratos, configuración y persistencia inicial. | Dependencias verificables sin acoplamiento entre repositorios. |
| 3 Parcela y cobertura | Registro de GeoJSON, versiones y consulta de insumos. | Casos de cobertura y permisos comprobados. |
| 4 Consulta de resultados | Resumen espacial de una ejecución compatible. | Nodata, escala y método de agregación explícitos. |
| 5 Ejecución bajo demanda | Adaptador, worker, cola y evidencia reproducible. | Ejecución aislada y reintentos controlados. |
| 6 Despliegue público | Frontend, API y almacenamiento accesibles. | Ensayo real, restauración y presupuesto revisados. |
| 7 Explicación y comparación | LLM o plantillas y alternativas habilitadas. | Afirmaciones respaldadas y límites de consumo activos. |
| Identificador | Decisión | Estado |
| --- | --- | --- |
| ADR 01 | Organizar el backend como monolito modular por bounded contexts. | Dirección acordada. |
| ADR 02 | Aplicar Domain, Application, Infrastructure e Interfaces en cada contexto. | Dirección acordada. |
| ADR 03 | Situar commands y queries de casos de uso en Application. | Recomendación; confirmar convención académica. |
| ADR 04 | Integrar CropSuiteLite con un puerto y un adaptador. | Dirección acordada. |
| ADR 05 | Ejecutar cálculos largos fuera del proceso HTTP. | Dirección acordada. |
| ADR 06 | Conservar snapshots, versiones y evidencia verificable. | Dirección acordada. |
| ADR 07 | Usar un VPS pequeño y servicios gratuitos para el inicio. | Presupuesto aceptado; proveedor pendiente. |
| ADR 08 | Ejecutar cultivos por turnos y limitar procesos internos. | Implementado en CLI; reutilización pendiente. |
| ADR 09 | Una parcela y varios cultivos, con resultados y fallos separados. | Implementado y probado con tres cultivos. |