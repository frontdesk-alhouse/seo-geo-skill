# GEO: base de evidencia (corte 2026-10-28)

> Qué mueve citas y menciones en ChatGPT, Google AI Overviews (AIO), AI Mode, Gemini, Perplexity,
> Claude y Copilot, separado por fuerza de evidencia. Todo lo demás del skill apunta aquí cuando
> necesita justificar una palanca.

**Etiquetas.** [E] evidenciado por estudio (casi siempre correlacional: asociación, no causa) ·
[O] oficial de la plataforma · [S] especulativo, vendor sin auditar o inferencia nuestra ·
[M] mito o contradicho por la evidencia · ⚠️ el dato llegó por cobertura secundaria, no por el
estudio original; se cita con esa advertencia.

---

## 1. Encuadre honesto (no negociable)

- **No hay ranking, no hay posición y no hay determinismo.** SparkToro/Gumshoe (ene-mar 2026) ⚠️:
  ~600 voluntarios, 12 prompts, ~3,000 corridas en UIs de consumo; menos de 1 en 100 de obtener la
  misma lista de marcas y menos de 1 en 1,000 el mismo orden [E]. La única métrica que aguanta es
  **% de visibilidad sobre muchas corridas**.
  https://searchengineland.com/ai-recommendation-lists-rarely-repeat-study-468076
- **El KPI es cita y mención, no tráfico.** Pew (2025-07-22, 900 adultos US): con resumen de IA el
  clic en resultado regular baja de 15% a 8%, y los enlaces dentro del resumen reciben ~1% de clics
  [E]. Reuters Digital News Report 2026 (97,520 encuestados, 48 mercados): ~4% hace clic a fuentes
  desde chatbots [E].
- **Nada es un interruptor.** Ninguna palanca (schema, llms.txt, longitud de párrafo) garantiza
  aparecer. Lo que se vende es superficie citable, entidad consistente y medición honesta.

## 2. Qué está evidenciado

### 2.1 Contenido de la página

| Hallazgo | Etiqueta | Fuente |
|---|---|---|
| Agregar citas textuales +40.9%, estadísticas +30.6%, fluidez +28.0%, citar fuentes +27.5%, términos técnicos +17.6%, tono autoritativo +10.4%; keyword stuffing −8.3% (visibilidad ajustada por posición) | [E] motores simulados 2023 | Princeton, Aggarwal et al., arXiv 2311.09735, KDD 2024. https://arxiv.org/html/2311.09735v3 |
| Las ganancias son grandes para la página en 5° lugar (citar fuentes +115%) y **negativas** para la 1ª (−30/−23/−21%); en Perplexity real: citas +22%, estadísticas +37% | [E] | Princeton, mismo paper |
| El paper **no** contiene ninguna regla de "134-167 palabras por pasaje" | [M] | Atribución falsa que circula en repos de GEO |
| Odds de ser citada vs ignorada (controlando DR y tipo de página): frescura ≤12 meses +88%, año en el título ×2, tablas +69% (ChatGPT +88%), metodología explicada en "best of" +51%, experiencia de primera mano +45%, precios visibles +28%, FAQ +26%, listas +22%, schema +13% | [E] asociación | TJ Robertson / TJ Digital, 2026-10-25. https://tjrobertson.com/ai-citation-study/ |
| Negativos en el mismo estudio: **byline de autor −28%**, CTAs −12%; muchas imágenes, lectura difícil y oraciones largas, leve | [E] asociación | TJ Robertson 2026-10-25 |
| Citadas abren con respuesta directa 20% vs 5%; 23% de citadas nunca responden la pregunta vs 50% de ignoradas; tono promocional igual (3.8 vs 3.7) | [E] | TJ Robertson 2026-10-25 |
| URLs citadas por IA promedian 1,064 días de antigüedad vs 1,432 en orgánico (25.7% más frescas); ChatGPT prefiere lo más nuevo, AIO apenas | [E] ~17M citas | Ahrefs. https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/ |

TJ Robertson en detalle: 78 negocios, 4,167 preguntas sin marca, 193,507 respuestas (ChatGPT,
AI Mode, AIO), 943,673 citas, 8 snapshots semanales (27-ago a 21-oct 2026). Limitaciones que
declara: asociación no es causa, keywords como proxy, muestra de clientes de Peec AI, sin dataset
descargable. Úsalo para priorizar, no para prometer porcentajes.

### 2.2 Qué tipo de página y qué sitio se cita

- Sitios de empresa reciben 67% de las citas (52% consumo/ecommerce, **87% B2B industrial**);
  página de producto 28%, home 12%, categoría 10%, perfil 9%, artículos ~25%; comparativas 2.5%,
  "alternatives to" 0.2% [E] (TJ Robertson 2026-10-25).
- Solo 2-5% de las páginas citadas vienen del top-10 de Google; AIO cita 24% del top-10, AI Mode
  17%, ChatGPT 7% [E] (TJ Robertson). Ahrefs (2026-03-02, 863k keywords): solo 38% de citas de AIO
  rankean top-10, contra 76% en jul-2025 [E].
  https://ahrefs.com/blog/ai-overview-citations-top-10/
- SE Ranking (feb 2026, 10k keywords US): 59% de citas de AI Mode a resultados orgánicos y **36% a
  perfiles de Google Business Profile** [E]. https://seranking.com/blog/ai-mode-research/

### 2.3 Menciones de terceros y entidad

- Ahrefs (2025-05-26, 75,000 marcas, AIO), Spearman con visibilidad: menciones web de marca 0.664,
  anchors de marca 0.527, volumen de búsqueda de marca 0.392, DR 0.326, backlinks 0.218 [E].
  https://ahrefs.com/blog/ai-overview-brand-correlation/
- Ahrefs (2025-12-12, ChatGPT + AI Mode + AIO): menciones en YouTube ~0.737, menciones web
  0.66-0.71 [E]. Ahrefs mismo advierte: correlación no es causa.
  https://ahrefs.com/blog/ai-brand-visibility-correlations
- Profound (ago 2024-jun 2025, 680M citas): ChatGPT cita primero Wikipedia (7.8%), Perplexity
  Reddit (6.6%); AIO reparte Reddit 2.2%, YouTube 1.9%, Quora 1.5%, LinkedIn 1.3% [E].
  https://www.tryprofound.com/blog/ai-platform-citation-patterns
- Semrush (ene-feb 2026, 325k prompts): LinkedIn citado en 14.3% de respuestas de ChatGPT Search y
  13.5% de AI Mode [E]. https://www.semrush.com/blog/most-cited-domains-ai/
- Yext (2025-10-09, 6.8M citas) [S vendor, vende listados]: 86% de citas desde fuentes que la marca
  gestiona (sitio 44%, listados 42%); en salud, listados 52.6%. **Muck Rack (2025)** ⚠️ dice lo
  contrario: ~84-94% de fuentes no propias. Lectura: la mezcla depende del tipo de consulta
  (informacional cita terceros; local y transaccional cita listados y sitio). Por eso la batería
  etiqueta cada consulta con `tipo_consulta`.

### 2.4 Local, reseñas y verticales

- BrightLocal (2026-08-26, 1,355 ubicaciones US/UK/AU, ~2M citas): GBP es la fuente principal de
  las IAs de Google (~28.6%); Yelp aparece en 80% de respuestas de ChatGPT; 93% de dominios citados
  son sitios de negocios individuales [E].
  https://www.brightlocal.com/resources/ai-directory-sources/
- 8ight.AI (2026-10-05, APIs con búsqueda, 39 oficios × 49 ciudades): negocios con <25 reseñas
  nombrados 3.4% vs 22.2% con 1,000+; **las estrellas no importan**; Claude citó Yelp en 92.7% vs
  ChatGPT 0%; Claude buscó solo en 36.6% de prompts [E, muestra chica de Claude: n=218, API,
  pendiente de replicar]. https://ppc.land/chatgpt-names-3-4-of-tested-local-firms-with-under-25-reviews-8ight-finds/
- Medical Economics (2026-08-25, ChatGPT, US, ~33k citas, 1,200 prompts de paciente): rosters
  hospitalarios y académicos 27.5%, consejos y asociaciones de especialidad 22.1%, directorios
  nacionales 8.3%, licencias estatales 5.1%, reseñas 3.8%; **cero citas a URLs de GBP**; los sitios
  de consultorio con páginas detalladas de procedimiento, candidatura y formación produjeron
  descripciones más específicas [E].
  https://www.medicaleconomics.com/view/before-you-pay-for-ai-visibility-for-your-practice-audit-these-five-sources
- Inmobiliario: Local Falcon (37,500 búsquedas, 100 ciudades US) solo 21.2% de agentes top con
  sitio fueron citados; portales y directorios dominan [E vendor].

### 2.5 Volatilidad, exactitud y tráfico

- Sistrix (abr 2026): AI Mode rota 56% de sus citas por semana, ChatGPT 74%; AIO estable en poco
  más de la mitad de las queries [E]. TJ Robertson: retención semana a semana 24-28%, a 7 semanas
  11-16% [E]. Consecuencia: N=3 por consulta y cadencia fija.
- Columbia Tow Center / CJR (mar 2025, 8 motores, 1,600 queries): >60% de respuestas con cita
  incorrecta; inventan URLs; ChatGPT Search totalmente correcto solo 28% [E]. Consecuencia: cada URL
  citada se abre y se verifica.
- Seer Interactive (sep 2025): CTR orgánico en queries con AIO cayó 61% desde mid-2024; marcas
  citadas en la AIO +35% clics orgánicos [E correlacional ⚠️].
  https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update
- Mención sin cita de respaldo: 31% en AI Mode, 25% en ChatGPT, 13% en AIO [E] (TJ Robertson).
  ChatGPT hace ~1.8 búsquedas por respuesta y agrega ubicación en 30% de preguntas sin ciudad [E].

### 2.6 Schema: el test nulo

- Ahrefs (may 2026): 1,885 páginas que agregaron JSON-LD vs 4,000 de control. AI Mode +2.4% y
  ChatGPT +2.2% (no significativos), AIO −4.6% [E]. Solo páginas ya citadas.
  https://www.searchenginejournal.com/schema-markup-didnt-move-ai-citations-in-ahrefs-test/574568/
- searchVIU: cinco sistemas de IA leen solo el HTML visible e ignoran el JSON-LD [E ⚠️].
- Bing sí declaró (mar 2025) que usa schema para sus LLMs [O].
- Lectura: schema es **comprensión de entidad e higiene**, no interruptor de citas. Se hace igual,
  porque es barato y alimenta rich results clásicos, pero no se vende como palanca GEO.

## 3. Qué dice Google oficialmente [O]

"AI features and your website" (2025-12-10)
https://developers.google.com/search/docs/appearance/ai-features

- No hay requisitos adicionales ni optimizaciones especiales para aparecer en AIO o AI Mode; no
  hace falta schema especial ni archivos de texto para IA. Cuenta estar indexado y ser elegible a
  snippet.
- El structured data debe ser consistente con el texto visible.
- Controles: `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`.
- AIO y AI Mode usan **query fan-out** (varias búsquedas por pregunta).
- El tráfico de AIO/AI Mode cuenta en Search Console dentro del tipo "Web".
- **Google-Extended** controla solo entrenamiento y grounding de Gemini; bloquearlo **no** te saca
  de AIO ni de AI Mode (eso solo lo hace bloquear Googlebot).
- Danny Sullivan (ene 2026): no trocear el contenido en "bite-sized chunks" para LLMs ni hacer
  dos versiones de la página.
- FAQ rich results dejaron de mostrarse el 2026-05-07; HowTo deprecado desde 2023.
- AI Mode en español, incluido México, desde 2025-09-23.
  https://blog.google/company-news/inside-google/around-the-globe/google-latin-america/google-mexico-20-years/
- Search Console "Generative AI" (beta desde 2026-06-03): solo impresiones, AIO + AI Mode + Discover
  combinados, sin clics.

## 4. Mitos y ventas que no se hacen

| Afirmación | Etiqueta | Por qué |
|---|---|---|
| "llms.txt te mete en ChatGPT" | [M] | John Mueller (jun 2025): ningún sistema de IA lo usa; luego "purely speculative". Ningún motor documenta usarlo. Ver `llms-txt.md` |
| "Agrega FAQPage para el rich result" | [M] | El rich result murió el 2026-05-07. El FAQ visible sí se asocia a citas (+26%, TJ Robertson), el schema no es la causa |
| "Schema = más citas en IA" | [M] | Test de Ahrefs may 2026 sin efecto significativo; Google dice que no hace falta |
| "Te posiciono en ChatGPT" | [M] | No hay posición; la misma lista se repite <1% de las veces |
| "Trocea el contenido para los LLMs" | [M] | Google (Sullivan, ene 2026) dice que no; lo que se asocia a citas es responder directo, no fragmentar |
| "Pasajes de 134-167 palabras" | [M] | No está en el paper de Princeton |
| "Score GEO de 0 a 100" con pesos | [M] | Los pesos son inventados; no hay estudio que los respalde. El skill reporta Índice de Citación con intervalo y censo de fuentes |
| "GPTBot alimenta ChatGPT Search" | [M] | El índice de búsqueda es OAI-SearchBot; GPTBot es entrenamiento. Ver `ai-crawlers.md` |

**Materiales de terceros desactualizados.** El skill de plugin `marketing:seo-audit` y cualquier
guía, plantilla o auditor que recomiende `FAQPage` o `HowTo` para obtener rich results está
desactualizado desde el 2026-05-07 (FAQ) y 2023 (HowTo). Igual para repos que atribuyen reglas de
longitud a Princeton o publican pesos de "score GEO". Si una herramienta lo sugiere, se ignora esa
recomendación y se deja constancia en el reporte.

## 5. El hueco en español y LatAm

- **No existe** estudio público de citas en AIO o AI Mode en español. Todo lo anterior es US/UK o
  global en inglés. Aplicarlo a México es inferencia [S].
- URBAN (2026-09-02, 276 respuestas a 46 prompts ES/EN) ⚠️: en preguntas sobre México, el medio más
  citado fue El País (13); el primer medio mexicano, El Financiero (7). Sugiere que los asistentes
  tiran de fuentes en español de España cuando no encuentran fuente mexicana sólida [S].
- StatCounter México (ago 2026): ChatGPT 75.1% del uso de chatbots, Gemini 16.7% [E]. Por eso la
  medición prioriza ChatGPT y Gemini, más AIO/AI Mode; Perplexity es opcional.
- Consecuencia práctica: la medición propia (`medicion-citacion.md`) **es** la evidencia local.
  Guarda las corridas; con el tiempo son el único dataset en español que tendrás.

## 6. Cronología de cambios (mid-2025 a oct-2026)

| Fecha | Cambio | Etiqueta |
|---|---|---|
| 2025-03 | Bing confirma que usa schema para sus LLMs; Claude declara Brave Search como subprocesador (2025-03-19) | [O] |
| 2025-03 | Tow Center: >60% de citas incorrectas | [E] |
| 2025-05-26 | Ahrefs: menciones de marca, mejor correlato de visibilidad en AIO | [E] |
| 2025-06 | Mueller: ningún sistema usa llms.txt | [O] |
| 2025-07-01 | Cloudflare bloquea bots de IA por defecto en zonas nuevas; pay-per-crawl en beta | [O] |
| 2025-07-22 | Pew: ~1% de clics en enlaces del resumen | [E] |
| 2025-08-04 | Cloudflare acusa a Perplexity de crawlers encubiertos | [O] |
| 2025-09-23 | AI Mode en español en México | [O] |
| 2025-10-09 | Yext 6.8M citas (vendor) | [S] |
| 2025-12-10 | Google publica "AI features and your website" | [O] |
| 2026-01 | Sullivan: no trocear contenido para LLMs | [O] |
| 2026-01 a 03 | SparkToro/Gumshoe: las listas casi nunca se repiten | [E] ⚠️ |
| 2026-02 | Bing Webmaster Tools AI Performance en preview; SE Ranking: 36% de citas de AI Mode a GBP | [O] / [E] |
| 2026-03-02 | Ahrefs: solo 38% de citas de AIO en top-10 | [E] |
| 2026-04 | Sistrix: AI Mode rota 56%/semana, ChatGPT 74% | [E] |
| 2026-05 | Ahrefs: schema sin lift en citas; Webflow AEO GA para Enterprise (2026-05-21); GA4 canal "AI Assistant" (2026-05-13) | [E] / [O] / ⚠️ |
| 2026-05-07 | Mueren los FAQ rich results | [O] |
| 2026-06-03 | Search Console "Generative AI" en beta | [O] |
| 2026-08 | BrightLocal (08-26) y Medical Economics (08-25) | [E] |
| 2026-09-15 | Cloudflare: control "Disallow AI Training" que en modo Block puede frenar Googlebot/Bingbot | [O] ⚠️ |
| 2026-10 | 8ight.AI (10-05) y TJ Robertson (10-25) | [E] |

## 7. Palancas priorizadas

Ordenadas por fuerza de evidencia y luego por esfuerzo. El detalle operativo vive en `geo-aeo.md`.

| Tier | Palanca | Evidencia | Esfuerzo |
|---|---|---|---|
| 1 | No bloquear bots de búsqueda (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot, Bingbot) y revisar Cloudflare del cliente | [O] | Bajo |
| 1 | Copy clave y JSON-LD en el HTML crudo (sin depender de JS) | [E] Vercel/MERJ dic 2024 | Bajo-medio |
| 1 | Respuesta directa al abrir cada página clave | [E] TJ Robertson | Bajo |
| 1 | Fecha visible, año en el título cuando aplique, actualización trimestral | [E] TJ Robertson, Ahrefs | Bajo |
| 1 | Medir con protocolo (N=3, Índice con intervalo, censo) antes de prometer nada | [E] SparkToro, Sistrix | Medio |
| 2 | Tablas comparativas, precios visibles, cifras con fuente, citas textuales | [E] TJ Robertson, Princeton | Medio |
| 2 | Superficies de terceros vivas y correctas: GBP, directorios del vertical, rosters, reseñas (conteo y ritmo) | [E] BrightLocal, SE Ranking, Medical Economics, 8ight | Medio |
| 2 | Experiencia de primera mano y metodología explicada | [E] TJ Robertson | Medio |
| 2 | Página propia que junte nombre + servicio + ciudad en la misma URL | [E] TJ Robertson (ubicación en 30% de búsquedas) + caso propio | Bajo |
| 3 | Menciones de marca en web, YouTube, LinkedIn, Reddit (sin comprarlas) | [E] correlacional Ahrefs, Semrush | Alto |
| 3 | Consistencia de entidad y `sameAs` verificado | [S] mecanismo razonable, sin test directo | Bajo |
| 3 | Bing Webmaster Tools + IndexNow como seguro | [O] / [S] | Bajo |
| 4 | Schema más allá del baseline | [E] nulo en citas | Bajo, se hace por SEO clásico |
| 4 | llms.txt | [M] como palanca | Bajo, cortesía |

Advertencias del mismo estudio que pesa más: el byline de autor se asocia a −28% y los CTAs a
−12%. No es razón para quitar autoría en YMYL (E-E-A-T manda ahí), pero sí para no llenar de CTAs
la página que quieres que se cite.
