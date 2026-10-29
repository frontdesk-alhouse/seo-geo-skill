# Entidad y sameAs: que el asistente sepa que todos esos perfiles son uno

> Consistencia de entidad, `sameAs` por vertical con fuentes mexicanas, reseñas y GBP como fuentes
> de cita, y auditoría de superficies de terceros. Etiquetas como en `geo-evidencia.md`.

---

## 1. Por qué importa

Los asistentes se alimentan de lo que terceros dicen del cliente, no solo de su sitio. Cuando las
superficies no coinciden pasan dos cosas, ambas vistas al medir casos reales:

1. **La identidad se parte.** La persona, su consultorio o empresa y su sitio aparecen como
   entidades distintas que el asistente no une. Cada una acumula una fracción de la señal, y en la
   consulta de marca el asistente mezcla datos o confunde al cliente con un homónimo.
2. **Una cifra falsa se propaga.** Un dato que el propio cliente escribió en un perfil (volumen de
   casos, años de experiencia, una certificación) se repite en corridas de varios asistentes y
   **sobrevive a su fuente**: sigue apareciendo aunque el perfil ya no exista. No se corrige
   hablándole al modelo; se corrige la fuente, y aun así tarda.

Encuadre honesto: la consistencia es **higiene**, no motor de aparición. Lo que hace aparecer es
la categoría angosta y la afirmación distintiva; la consistencia hace que lo que aparece sea
correcto y duradero [S, mecanismo razonable sin test directo]. Pero si el asistente manda a un
paciente al hospital equivocado, el daño es real.

## 2. Checklist de consistencia

Se llena una tabla con una fila por superficie y una columna por dato. Cualquier diferencia se
corrige en la superficie, no en la tabla.

| Dato | Regla |
|---|---|
| Nombre exacto | Una sola forma, igual en sitio, schema, GBP y directorios. Con o sin "Dr."/"Dra." y segundo apellido, pero siempre igual |
| Registro | Médico: cédula profesional y de especialidad (SEP). Empresa: razón social y RFC donde aplique. Inmobiliario: registro AMPI o estatal si existe |
| Formación | Mismas instituciones y años. Un curso no es fellowship; no se infla |
| Instituciones | Hospitales, clínicas, cámaras o asociaciones vigentes. Quitar las que ya no aplican |
| NAP | Nombre, dirección y teléfono idénticos (ver `local-seo.md`) |
| Categoría | La misma categoría principal en GBP, directorios y schema |
| Cifras | Solo cifras verificables y publicadas en el sitio con fecha |

**Regla dura:** ninguna credencial ni cifra entra a una superficie pública sin estar verificada.
En SEO clásico un error se corrige editando la página; aquí se replica.

## 3. sameAs por vertical

`sameAs` en el schema de `Person` u `Organization` declara qué perfiles son la misma entidad. Es la
desambiguación más barata, y crítica cuando existe un homónimo. Solo se listan perfiles **propios
o verificados de la entidad**, vivos, que digan lo mismo que el sitio.

| Vertical | Superficies candidatas (México) |
|---|---|
| **Médico** | Doctoralia, Topdoctors.mx, doktor.mx, perfil del consejo de certificación de la especialidad (ver CONACEM), registro de cédula profesional SEP, rosters de hospitales donde opera (página del médico en el hospital), asociación o colegio de la especialidad, ORCID, Google Scholar (PubMed no tiene perfil de autor: sus artículos se anclan vía ORCID, no con una URL de búsqueda), GBP del consultorio, LinkedIn |
| **SaaS** | LinkedIn de la empresa, Crunchbase, G2, Capterra, Product Hunt, GitHub de la organización, perfiles de los fundadores (como `Person` aparte) |
| **B2B industrial** | LinkedIn, GBP de planta y oficinas, cámaras (CANACINTRA, COPARMEX, cámara del sector), directorios industriales del sector y de parques industriales, registros de proveedor en portales de compra de clientes grandes cuando son públicos |
| **Inmobiliario** | Portales donde publica (perfil de agencia, no anuncios sueltos), AMPI (sección local), GBP, LinkedIn, Instagram si es el canal real |

Notas por vertical:

- **Médico.** Medical Economics (2026-08-25, ChatGPT, US) encontró que rosters hospitalarios y
  académicos (27.5%) y perfiles de consejo o asociación (22.1%) son las fuentes que más cita
  ChatGPT para médicos, y **cero citas a URLs de GBP** [E, US]. Prioridad: que el hospital tenga
  una página del médico con nombre, especialidad y formación correctas. Un ancla de autor real
  (ORCID, PubMed, Scholar) dura más que un directorio comercial.
- **B2B industrial.** TJ Robertson (2026-10-25): 87% de las citas en B2B industrial van a sitios de
  empresa [E]. La palanca es el sitio propio; los directorios son respaldo de entidad.
- **Inmobiliario.** Local Falcon: portales y directorios dominan, solo 21.2% de agentes top con
  sitio fueron citados [E vendor, US]. El perfil de agencia en portales importa tanto como el sitio.
- **SaaS.** Semrush (ene-feb 2026): LinkedIn citado en 14.3% de respuestas de ChatGPT Search [E].
  G2 y Capterra entran en consultas de comparación.

**Wikidata solo si la entidad es notable** (prensa independiente, publicaciones, premios
verificables). Crear un ítem para un consultorio o una pyme sin fuentes secundarias es spam, lo
borran, y deja rastro.

**Cada URL de `sameAs` se abre y debe decir lo mismo.** Antes de publicar el schema y en cada
corrida trimestral. Un `sameAs` a un perfil muerto o contradictorio empeora la entidad. Nunca se
adivina una URL (ver `saas.jsonld.md`).

## 4. Reseñas como fuente

- 8ight.AI (2026-10-05, APIs con búsqueda): negocios con menos de 25 reseñas fueron nombrados en
  3.4% de las respuestas, contra 22.2% con 1,000 o más; **las estrellas no importaron** [E,
  pendiente de replicar].
- En directorios médicos con suscripción, el orden lo mueve el **ritmo de reseñas nuevas**, no el
  promedio de estrellas (observación propia, [S]).
- Lectura: lo que cuenta es **conteo y ritmo**, no la calificación. El plan es pedir reseña de
  forma sistemática después de cada servicio, en la superficie que el vertical usa.

## 5. Google Business Profile como fuente de cita

| Estudio | Hallazgo | Para quién |
|---|---|---|
| SE Ranking, feb 2026 | 36% de citas de AI Mode apuntan a GBP [E] | Local en Google |
| BrightLocal, 2026-08-26 | GBP es la fuente principal de las IAs de Google (~28.6%) [E] | Local en Google |
| Medical Economics, 2026-08-25 | 0 citas a GBP en ChatGPT para médicos [E] | Médicos en ChatGPT |

Lectura: GBP se audita como fuente de cita para AIO y AI Mode (categoría, descripción, servicios,
horario, fotos, respuestas a reseñas), pero no se vende como la palanca para ChatGPT en salud. Ahí
pesan rosters, consejos y el sitio propio con páginas detalladas.

## 6. Auditoría de superficies de terceros

Una vez por cliente al inicio, y luego con el censo de fuentes de cada medición
(`medicion-citacion.md`).

1. Buscar el nombre exacto y variantes en Google, Bing y dentro de los directorios del vertical.
2. Listar cada superficie: URL, dueño (propia, gestionada, de tercero), estado (viva, muerta,
   bloqueo anti-bot), fecha de última edición si se ve.
3. Comparar contra el checklist de la sección 2.
4. Cruzar con el censo de fuentes: ¿qué superficies citan los asistentes de verdad? Esas van
   primero.
5. Plan: corregir las vivas que se citan, reclamar las que se pueden reclamar, pedir baja o
   corrección de las que tienen datos falsos, y redirigir (301) dominios o páginas viejas del
   cliente a la URL canónica.

Verificación de estado: con navegador, no solo con script. Un 404 o 403 con UA de bot puede ser
bloqueo anti-bot. Y una superficie que hoy sostiene al cliente puede desaparecer en semanas; por
eso se audita en cada ciclo.

Planeación: **una superficie de tercero viva y correcta vale más, y antes, que un sitio que
todavía no existe.** Corregir un perfil de directorio puede rendir mientras el sitio se construye.

## 7. Qué NO hacer

- **No comprar menciones en listas de "los mejores"** presentadas como editorial. Si lo pagaste, la
  regulación publicitaria aplica igual, y en salud es una violación.
- **No copiar reseñas de terceros** al sitio ni marcarlas en schema: Google prohíbe agregar ratings
  ajenos.
- **Salud (COFEPRIS):** en perfiles, bios y descripciones de directorio no van los claims
  prohibidos ("la técnica más avanzada", "menor tiempo de recuperación", "resultados garantizados",
  "la cirugía más segura", "el mejor tratamiento", "sin riesgos"). Lo que se repite en un
  directorio se repite en el asistente.
- No crear perfiles duplicados para "tener más presencia": parten la entidad.
- No llenar perfiles con cifras que no estén publicadas y respaldadas en el sitio.
- No poner en `sameAs` perfiles de otra persona, de la clínica cuando el `Person` es el médico, ni
  páginas de búsqueda.
