# Batería de prompts: {{NOMBRE}}

Plantilla para medir si los asistentes de IA nombran a un negocio cuando alguien pregunta por lo que vende, sin mencionarlo y mencionándolo. Método completo, justificación de N y cadencia: `references/medicion-citacion.md`. Bots y búsqueda: `references/ai-crawlers.md`.

- Cliente: {{NOMBRE}}
- Servicio o categoría: {{SERVICIO}}
- Ciudad o mercado: {{CIUDAD}}
- Vertical: {{médico | SaaS | B2B industrial | inmobiliario | otro}}
- Fecha de alta del set: {{AAAA-MM-DD}}
- Responsable de las corridas: {{persona}}

## Protocolo

| Aspecto | Regla |
|---|---|
| Asistentes | ChatGPT y Gemini siempre. Claude recomendado. Google AI Overviews y AI Mode en navegador cuando la consulta los dispare. Perplexity y Copilot opcionales (Perplexity pide cuenta). Cada asistente se reporta por separado: no se promedian entre sí. |
| N | 3 corridas por consulta y asistente, en la misma ventana de fechas. Las respuestas no se repiten entre corridas; por eso nunca se reporta una sola. |
| Sesión | ChatGPT: chat temporal, con "Unpersonalized" visible en el encabezado. Gemini: chat temporal. Claude: incógnito con búsqueda web activada. AI Overviews y AI Mode: ventana privada. Se anota el modo exacto en cada corrida (`modo`). |
| Idioma | Español de México, tal como escribiría la persona. Sin corregir errores de dedo si la batería los incluye a propósito. |
| Qué se registra | Un archivo por corrida con `templates/corrida.template.md`: verbatim completo, orden de nombres, posición del cliente, URLs citadas, si buscó en la web, cifras pegadas al nombre, modo, fecha y notas. |
| Verificación | Cada URL citada se abre con `scripts/verificar_fuentes.py` y, si sale `bloqueo-anti-bot`, en un navegador real. Una fuente puede estar muerta o no decir lo que el asistente dijo. |

**Regla de inmutabilidad.** El set no se modifica entre corridas: ni se reformula, ni se corrigen acentos, ni se quitan consultas que "salen mal". Una consulta nueva se agrega al final con id nuevo, fecha de alta y la marca "sin histórico" hasta que tenga dos ciclos. Una consulta retirada conserva su id y se marca "retirada (fecha)"; su id no se reutiliza.

**Variable no controlada (declárala en cada reporte).** Las corridas se hacen con sesiones reales, en un país y desde una IP concretos. Aunque el modo sea temporal o incógnito, el asistente puede usar la ubicación aproximada (ejemplo típico: "según tu ubicación actual..."). N=3 sobre sistemas no deterministas es una señal comparable en el tiempo, no una medición limpia.

**Tipo de consulta.** Cada consulta se etiqueta una sola vez como `informacional` (quiere entender), `local` (busca a alguien en un lugar) o `transaccional` (quiere comprar, cotizar o agendar). La mezcla de fuentes que citan los asistentes cambia según el tipo, así que el índice se lee también por tipo.

## Familias

| Familia | Qué mide | Obligatoria |
|---|---|---|
| F1 | Sin marca, por necesidad o padecimiento: ¿te nombran cuando alguien busca lo que haces? | Sí |
| F2 | Sin marca, por decisión: ¿apareces cuando la persona todavía decide si lo necesita o cuánto cuesta? | Sí |
| F3 | Con marca: ¿el asistente sabe quién eres, sin confundirte? Incluye la prueba del homónimo. Se reporta aparte, nunca suma al subtotal sin marca. | Sí |
| F4 | El tercero que busca por él: familiar, jefe, área de compras. | Sí |
| F5 | Caso específico: un padecimiento, problema o escenario angosto donde el cliente es fuerte. | Opcional |
| F6 | Técnica, método o producto con nombre propio. | Opcional |

Cuántas: 2 a 4 consultas por familia obligatoria y 1 a 3 por opcional. Más consultas no compensan menos corridas.

## Ejemplos por vertical (ficticios, para adaptar)

Sustituye los placeholders. No copies ejemplos de otro vertical sin reescribirlos con el lenguaje real de la audiencia.

### F1: sin marca, por necesidad o padecimiento

| Vertical | Consulta | tipo_consulta |
|---|---|---|
| Médico | ¿Quién es el mejor {{SERVICIO}} en {{CIUDAD}}? | local |
| Médico | Me duele la espalda baja desde hace meses y me baja a la pierna, ¿qué especialista me puede ver en {{CIUDAD}}? | local |
| SaaS | ¿Qué {{SERVICIO}} me recomiendas para una empresa de 50 personas en México? | transaccional |
| SaaS | Necesito dejar de hacer la nómina en Excel, ¿qué herramientas hay? | informacional |
| B2B industrial | ¿Qué proveedores de {{SERVICIO}} hay en {{CIUDAD}}? | local |
| B2B industrial | Necesito un fabricante de {{SERVICIO}} con certificación para la industria automotriz en el Bajío | transaccional |
| Inmobiliario | ¿Qué desarrollos de {{SERVICIO}} hay en {{CIUDAD}}? | local |
| Inmobiliario | Busco departamento de dos recámaras cerca de mi trabajo en {{CIUDAD}}, ¿dónde conviene? | local |

### F2: sin marca, por decisión

| Vertical | Consulta | tipo_consulta |
|---|---|---|
| Médico | Tengo hernia de disco, ¿de verdad necesito cirugía? | informacional |
| Médico | ¿Cuánto cuesta una cirugía de {{SERVICIO}} en {{CIUDAD}}? | transaccional |
| Médico | ¿Cómo sé si un cirujano está certificado en México? | informacional |
| SaaS | ¿Vale la pena pagar un {{SERVICIO}} o lo hago con hojas de cálculo? | informacional |
| SaaS | ¿Cuánto cuesta un {{SERVICIO}} para una pyme en México? | transaccional |
| B2B industrial | ¿Qué debo pedirle a un proveedor de {{SERVICIO}} antes de darlo de alta? | informacional |
| B2B industrial | ¿Conviene importar {{SERVICIO}} o comprarlo a un fabricante nacional? | informacional |
| Inmobiliario | ¿Conviene comprar en preventa o un departamento ya terminado en {{CIUDAD}}? | informacional |
| Inmobiliario | ¿Cuánto cuesta el metro cuadrado en {{CIUDAD}} este año? | transaccional |

### F3: con marca (incluye la prueba del homónimo)

| Vertical | Consulta | tipo_consulta |
|---|---|---|
| Todas | ¿Quién es {{NOMBRE}}? (sin ciudad ni contexto: prueba del homónimo, ¿te confunde con otra persona o empresa del mismo nombre?) | informacional |
| Todas | {{NOMBRE}} {{CIUDAD}}, ¿qué opiniones tiene? | informacional |
| Médico | ¿Dónde atiende {{NOMBRE}} y cómo agendo consulta? | transaccional |
| SaaS | ¿Qué hace {{NOMBRE}} y en qué se diferencia de sus alternativas? | informacional |
| B2B industrial | ¿{{NOMBRE}} tiene certificaciones y a qué industrias surte? | informacional |
| Inmobiliario | ¿{{NOMBRE}} es una desarrolladora confiable? ¿Ha entregado a tiempo? | informacional |

Al registrar F3: si el asistente mezcla datos de un homónimo, anótalo en `notas` y cualquier dato falso en `cifra_pegada`.

### F4: el tercero que busca por él

| Vertical | Consulta | tipo_consulta |
|---|---|---|
| Médico | Mi papá tiene estenosis lumbar, ¿a quién lo llevo en {{CIUDAD}}? | local |
| Médico | ¿Cómo elijo un buen {{SERVICIO}} para mi mamá? | informacional |
| SaaS | Mi jefe me pidió comparar opciones de {{SERVICIO}}, ¿cuáles debo revisar? | transaccional |
| SaaS | Soy contador externo de varias pymes, ¿qué {{SERVICIO}} les recomiendo? | transaccional |
| B2B industrial | Compras me pidió tres cotizaciones de {{SERVICIO}} en {{CIUDAD}}, ¿a quién le pido? | transaccional |
| B2B industrial | Soy ingeniero de planta, ¿qué proveedor de {{SERVICIO}} responde rápido en paros de línea? | local |
| Inmobiliario | Mis papás quieren comprar para retirarse en {{CIUDAD}}, ¿qué desarrollos son buenos? | local |
| Inmobiliario | Me mudo a {{CIUDAD}} por trabajo, ¿en qué zona y con quién busco depa? | local |

### F5 (opcional): caso específico

| Vertical | Consulta | tipo_consulta |
|---|---|---|
| Médico | Me operaron de columna hace dos años y volvió el dolor, ¿quién hace cirugías de revisión en {{CIUDAD}}? | local |
| Médico | Tengo escoliosis de adulto, ¿quién la trata en {{CIUDAD}}? | local |
| SaaS | ¿Qué {{SERVICIO}} maneja bien empleados en varios estados con distintas prestaciones? | transaccional |
| SaaS | ¿Hay algún {{SERVICIO}} que se integre con el timbrado de CFDI sin programar? | informacional |
| B2B industrial | ¿Quién fabrica {{SERVICIO}} para alta temperatura en México? | transaccional |
| B2B industrial | ¿Quién da mantenimiento a {{SERVICIO}} de marca europea en {{CIUDAD}}? | local |
| Inmobiliario | ¿Qué desarrollos en {{CIUDAD}} aceptan crédito Infonavit más crédito bancario? | transaccional |
| Inmobiliario | ¿Dónde hay departamentos que admitan mascotas grandes en {{CIUDAD}}? | local |

### F6 (opcional): técnica, método o producto con nombre propio

| Vertical | Consulta | tipo_consulta |
|---|---|---|
| Médico | ¿Quién hace cirugía endoscópica de columna en {{CIUDAD}}? | local |
| Médico | ¿Qué es la artrodesis lumbar mínimamente invasiva y quién la hace en México? | informacional |
| SaaS | ¿Qué es {{TÉRMINO PROPIO DEL PRODUCTO}} y qué herramientas lo hacen? | informacional |
| SaaS | ¿Qué {{SERVICIO}} tiene conciliación automática con el banco? | transaccional |
| B2B industrial | ¿Quién en México hace recubrimiento por {{PROCESO}} para piezas de {{MATERIAL}}? | transaccional |
| B2B industrial | ¿Qué diferencia hay entre {{PROCESO A}} y {{PROCESO B}} y quién los ofrece en {{CIUDAD}}? | informacional |
| Inmobiliario | ¿Qué desarrollos en {{CIUDAD}} tienen certificación de edificación sustentable? | local |
| Inmobiliario | ¿Qué es el esquema de copropiedad fraccionada y quién lo ofrece en {{CIUDAD}}? | informacional |

## Set del cliente (inmutable)

| id | familia | tipo_consulta | consulta | alta | estado |
|---|---|---|---|---|---|
| Q-01 | F1 | | | {{AAAA-MM-DD}} | activa |
| Q-02 | F1 | | | {{AAAA-MM-DD}} | activa |
| Q-03 | F2 | | | {{AAAA-MM-DD}} | activa |
| Q-04 | F2 | | | {{AAAA-MM-DD}} | activa |
| Q-05 | F3 | | ¿Quién es {{NOMBRE}}? | {{AAAA-MM-DD}} | activa |
| Q-06 | F3 | | | {{AAAA-MM-DD}} | activa |
| Q-07 | F4 | | | {{AAAA-MM-DD}} | activa |
| Q-08 | F4 | | | {{AAAA-MM-DD}} | activa |

Estados: `activa`, `sin histórico (alta AAAA-MM-DD)`, `retirada (AAAA-MM-DD)`.

## Registro de corridas

Una fila por corrida. El detalle vive en el archivo de la corrida; esta tabla es el índice para no perder ninguna.

| Fecha | id | Asistente | Corrida | Modo | Buscó | Aparece | Posición | Archivo | Incidentes |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

Nombre sugerido de archivo: `Q-01_chatgpt_c1.md`. Al cerrar el ciclo: `python3 scripts/indice_citacion.py <carpeta> --n-esperado 3`.

## Gotchas de ejecución

- **Prellenado por URL en ChatGPT.** Abre `https://chatgpt.com/?temporary-chat=true&q=<consulta urlencoded>` y da clic en enviar. Teclear con automatización de navegador (`type`) falla con acentos y signos de apertura. En Gemini y Claude se teclea o se pega.
- **Lotes cortos.** Si automatizas con una extensión de navegador, mantén cada lote de acciones en 40 segundos o menos. Un lote que se agota pierde la corrida en silencio: confirma que el archivo quedó escrito antes de pasar a la siguiente.
- **Verifica el modo antes de enviar.** Si no ves "chat temporal" o "Unpersonalized", la corrida no cuenta: repítela y anota el incidente.
- **Ubicación.** Si la respuesta menciona tu ubicación ("cerca de ti", "en tu ciudad"), anótalo en `notas`: es la variable no controlada en acción.
- **Una pestaña a la vez.** Algunas interfaces no generan la respuesta si la pestaña está oculta; trabaja con la pestaña visible.
- **No reformules a mano.** Si una consulta parece mal escrita, se queda así en este ciclo y la versión nueva entra al final con id nuevo.
