# GEO / AEO: readiness on-site y palancas de citación en asistentes de IA

> Portado y adaptado de conceptos de `AgriciDaniel/claude-seo` (v2.2.4, MIT).
> Actualizado en 2026 con criterios operativos de un caso SaaS y el procedimiento
> de medición de un caso médico; actualizado 2026-10-28 con la base de evidencia de
> `geo-evidencia.md` (etiquetas [E] estudio · [O] oficial · [S] inferencia · [M] mito).

GEO (Generative Engine Optimization) / AEO (Answer Engine Optimization) es la evolución del SEO
para un SERP donde muchas queries muestran una respuesta generada por IA, y para un mundo donde
mucha gente ya ni pasa por el SERP: le pregunta directo a un asistente.
Riesgo: zero-click. Oportunidad: ser la fuente citada.

**Encuadre honesto, y no es negociable.** En un asistente **no hay ranking, no hay posición y no
hay determinismo**. La misma pregunta repite la misma lista de marcas menos de 1 vez en 100
(SparkToro/Gumshoe, 2026 [E] ⚠️). Lo que sí se puede ofrecer es superficie citable, entidad
consistente y **medición honesta**. El KPI es cita y mención, no tráfico. Prometer "te posiciono
en ChatGPT" es la versión 2026 de prometer ranking por schema.

---

## Lo que de verdad mueve la aguja

Doce palancas en dos bloques, cada una con su etiqueta. La evidencia completa y el orden por
prioridad (Tier 1-4) están en `geo-evidencia.md` §7.

### Estructura del contenido

1. **Respuesta directa al abrir** [E]. Las páginas citadas abren respondiendo 20% de las veces vs
   5% de las ignoradas; 23% de las citadas nunca responden la pregunta vs 50% de las ignoradas (TJ
   Robertson, 2026-10-25). Nada de intro de relleno antes de la respuesta.
2. **Pasajes autocontenidos** [S]. Cada bloque clave debe entenderse sin el resto de la página:
   pregunta implícita, respuesta, contexto. No hay longitud mágica: la regla de "134-167 palabras"
   que circula **no está** en el paper de Princeton [M]. Y no se trocea la página para los LLMs:
   Google lo desaconseja (Sullivan, ene 2026 [O]).
3. **Datos concretos con fuente**, no adjetivos [E]. Estadísticas +30.6%, citas textuales +40.9%,
   citar fuentes +27.5% (Princeton, KDD 2024, motores simulados). *"montaje de una nave de 5,000 m² en
   10 semanas"* se cita; *"resultados increíbles"* no.
4. **Tablas y estructura comparativa** [E]. Tablas +69% en odds de cita (ChatGPT +88%), listas
   +22% (TJ Robertson). Tablas de capas, criterios y límites: es lo que el modelo reusa tal cual.
5. **Frescura visible** [E]. Contenido actualizado en los últimos 12 meses +88%; año en el título
   ×2 (TJ Robertson); URLs citadas 25.7% más frescas que las orgánicas (Ahrefs). Fecha visible de
   actualización y revisión trimestral real, no cambiar la fecha sin cambiar el contenido.
6. **Precios visibles** [E] +28% (TJ Robertson). Si hay precio o rango, publicarlo; si no se
   publica, decirlo.
7. **Experiencia de primera mano y metodología** [E]. Primera mano +45%; en páginas "los mejores X",
   explicar cómo se eligió +51% (TJ Robertson). Casos propios, fotos propias, proceso real.
8. **Postura clara y nombrable** [S, caso propio]. *"el CRM que se llena solo desde WhatsApp"* es citable; *"la mejor
   plataforma"* no.
9. **Decir lo que el producto o el médico NO hace** [S, caso propio]. Los modelos reusan el
   contenido que acota, y es lo único que distingue de verdad en una categoría saturada.

**Advertencias del mismo estudio** [E, asociación]: el **byline de autor** se asocia a −28% y los
**CTAs** a −12%. En YMYL la autoría se queda (E-E-A-T manda), pero no se llena de CTAs la página que
se quiere citar. Schema solo +13%, y en el test controlado de Ahrefs (may 2026) sin efecto
significativo.

### Entidad y autoridad

10. **Claridad de entidad y `sameAs`** [S]. Schema (`Organization`, `Person`, `Product`,
    `MedicalClinic`) y `sameAs` declaran qué es cada cosa y qué perfiles son la misma entidad. Es la
    desambiguación más barata y crítica con homónimos. Su valor es comprensión de entidad, no
    interruptor de citas. Detalle en `entidad-sameas.md`.
11. **Superficies de terceros y E-E-A-T demostrable** [E]. Menciones web de marca son el mejor
    correlato de visibilidad en AIO (Spearman 0.664, Ahrefs 2025); GBP recibe 36% de citas de AI
    Mode (SE Ranking, feb 2026); en médicos, ChatGPT cita rosters hospitalarios y consejos de
    especialidad, no GBP (Medical Economics, 2026-08). Autor con credenciales, fecha y fuentes;
    para una persona, un ancla de autor real (ORCID, Google Scholar) dura más que un directorio
    comercial.
12. **Categoría angosta** [S, caso propio]. Un asistente contesta con nombre propio cuando el
    conjunto de respuestas defendibles es chico. En una categoría poblada elige agregadores; en una
    angosta elige personas. **Si el cliente está en una categoría saturada, angostar la categoría
    es más barato que ganarla.**

---

## Lo que este canal hace distinto (hallazgos de medir casos reales)

Salieron de medir un caso médico (decenas de corridas en tres asistentes, 2026) y un caso SaaS. Son principios, no
promesas; cambian cómo se planea.

1. **Se alimenta de lo que terceros dicen, no solo del sitio.** En el caso medido, el sitio propio
   no resolvía y aun así el asistente describía al cliente con precisión, con el lenguaje literal
   de un perfil de directorio. **Una superficie de tercero viva vale más, y antes, que un sitio que
   todavía no existe.** Reescribir el perfil de directorio puede rendir más que esperar al build.
2. **La identidad se parte en entidades que el asistente no une** (persona, centro, sitio). Cada
   una acumula una fracción de la señal. Se corrige con `sameAs`, nombre exacto en todas partes y
   redirecciones 301 de dominios y páginas viejas.
3. **Una cifra falsa se propaga y sobrevive a su fuente.** Un dato que el propio cliente escribió en
   un perfil, sin validar y contradicho por otra cifra suya, apareció en 7 corridas aunque el perfil
   ya no respondía. **No se corrige hablándole al modelo: se corrige la fuente**, y aun así tarda.
   Regla dura: ninguna credencial ni cifra entra a una superficie pública sin estar verificada.
4. **Los competidores que ganan entran por sitio propio con nombre + técnica + ciudad en la misma
   URL.** ChatGPT agrega ubicación en 30% de las preguntas sin ciudad (TJ Robertson [E]): la página
   tiene que nombrar servicio y ciudad juntos.
5. **El asistente declara su criterio, y hay que publicarlo.** En el caso médico, los tres
   asistentes eligieron por "cuántas cirugías de ese tipo hace al año". Si existe la cifra
   verificable, se publica con su respaldo y fecha; si no, no se inventa.
6. **Claude ≠ ChatGPT ≠ Gemini.** Índices distintos, fuentes distintas, tasas de búsqueda distintas
   (Claude buscó en 36.6% de prompts en 8ight.AI 2026 [E, muestra chica]). Se mide y se reporta por
   asistente, nunca un promedio.
7. **La fuente que te sostiene puede desaparecer en semanas** (en el caso medido, 13 días). Por eso
   la medición se repite y el censo de fuentes se audita en cada ciclo.

Y una trampa de verificación: una ficha de directorio que parecía dar 404 era **bloqueo anti-bot**.
Antes de reportar una fuente como muerta, verificar con UA de navegador.

**La consistencia de entidad es higiene, no motor.** En el caso medido la entidad estaba
fragmentada y contradictoria, y aun así lo citaban: lo hacía aparecer la categoría angosta más la
afirmación distintiva. La consistencia hace que lo citado sea **correcto y duradero**. No se vende
como palanca de aparición. Y si el asistente manda al paciente al hospital equivocado, el daño es
real.

---

## Cómo se mide (resumen)

Protocolo completo en `medicion-citacion.md`; cálculo con `scripts/indice_citacion.py`.

- Batería fija en familias F1-F4 (+F5/F6 opcionales), etiquetada por `tipo_consulta`. **No se
  modifica entre corridas**; lo nuevo va al final con fecha de alta.
- N=3 por consulta y asistente, en la **UI de consumo** con sesión temporal; la sesión es variable
  no controlada declarada.
- Prioridad en México: ChatGPT, Gemini, AIO/AI Mode, Claude; Perplexity opcional.
- Se registran nombres, posición, URLs citadas, si buscó y la cifra pegada al nombre; cada URL se
  verifica (`scripts/verificar_fuentes.py`).
- Índice de Citación con intervalo de Wilson al 95%, subtotal sin marca, primer lugar, tasa de
  disparo y censo de fuentes. Nunca un "score GEO" compuesto.
- Cadencia: línea base, +30 y +60 días tras cambios, luego trimestral; ChatGPT y AI Mode mensual
  como mínimo porque rotan 74% y 56% de citas por semana (Sistrix, abr 2026 [E]).
- Y lo que vale más: preguntarle a los clientes del cliente **cómo llegaron**, con "asistente de IA"
  como opción explícita.

---

## Cómo aplicarlo en el build

- Al menos un **bloque de respuesta directa** por página clave: pregunta real de la audiencia,
  respuesta de un párrafo autocontenido al abrir, cifra con fuente y fecha.
- Encabezados en forma de pregunta cuando calce la intención (*"¿Cuánto dura la recuperación de
  una cirugía de columna?"*).
- Una tabla donde haya comparación real (opciones, criterios, rangos de precio, límites).
- Fecha de actualización visible; año en el título cuando el contenido es de temporada o de precio.
- Copy clave y JSON-LD en el **HTML crudo**, no inyectados por JS (ver `ai-crawlers.md`).
- Schema alineado con ese contenido, **con `sameAs` poblado** hacia perfiles reales y verificados.
- Ancla de autor donde exista material real.
- robots.txt sin bloquear bots de búsqueda de IA (`ai-crawlers.md`); llms.txt opcional como
  cortesía (`llms-txt.md`); canal de IA en GA4 y Bing Webmaster Tools (`analytics-ia.md`).

## Qué NO hacer

- **No prometer posición ni ranking en ningún asistente.** No existen.
- **No confundir AEO con volver a meter `FAQPage`** esperando rich result visual: murió el
  2026-05-07. El FAQ visible sí ayuda a responder; el schema no es la causa.
- **No "escribir para el robot"** ni trocear la página en fragmentos. Se citan los pasajes claros.
- **No vender llms.txt ni schema como palanca de citas** [M].
- **No fabricar la afirmación distintiva.** Si el hecho angosto y verificable no existe, no existe.
- **No comprar menciones en listas de "los mejores"** presentadas como editorial. Que lo diga un
  tercero no te libra de la regulación publicitaria si tú lo pagaste, y en salud es una violación.
- **No copiar reseñas de terceros a tu sitio** para parecer más citable: Google prohíbe agregar
  ratings ajenos.
