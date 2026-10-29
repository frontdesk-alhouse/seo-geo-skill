# Medición de citación en asistentes de IA (protocolo manual)

> Cómo medir si un cliente aparece en ChatGPT, Gemini, Google AIO/AI Mode, Claude o Perplexity, de
> forma que la serie sea comparable en el tiempo. Sin API, sin herramienta paga: navegador, una
> plantilla y un script de cálculo.
> Plantillas: `templates/bateria-prompts.template.md`, `templates/corrida.template.md`.
> Scripts: `scripts/indice_citacion.py`, `scripts/verificar_fuentes.py`.

**Lo que esto es y lo que no.** N=3 sobre sistemas no deterministas, corrido desde una cuenta real,
es una **señal comparable en el tiempo**, no una medición limpia. Se reporta como rango, nunca
como posición.

---

## 1. La batería de consultas

Se escribe una vez por cliente, antes de la primera corrida.

| Familia | Qué mide | Ejemplo ficticio (médico: Dra. Elena Ruiz, cirugía de columna, Monterrey) |
|---|---|---|
| **F1** Sin marca, por necesidad | Si el cliente existe en el canal | "¿Quién es el mejor cirujano de columna en Monterrey?" |
| **F2** Sin marca, por decisión | La pregunta previa a comprar | "Tengo una hernia de disco, ¿de verdad necesito cirugía?" · "¿Cuánto cuesta una cirugía de columna en Monterrey?" |
| **F3** Con marca | Qué dice de él y si lo confunde | "¿Quién es la Dra. Elena Ruiz?" · "Dra. Elena Ruiz, ¿dónde atiende?" · prueba del homónimo |
| **F4** El tercero que busca por él | Familiar, socio, comité de compra | "Mi papá tiene estenosis lumbar, ¿a quién veo en Monterrey?" |
| F5 opcional, caso específico | Padecimiento o caso puntual | "¿Quién opera escoliosis en adultos en Monterrey?" |
| F6 opcional, técnica | Técnica o método nombrable | "¿Quién hace cirugía endoscópica de columna en Nuevo León?" |

Equivalentes en otras verticales: SaaS (Nimbus CRM): F1 "mejor CRM para equipos de ventas en
México", F2 "¿HubSpot o un CRM local para 10 vendedores?", F4 "mi jefe quiere un CRM, ¿cuál le
propongo?". B2B (Aceros del Bajío): F1 "fabricantes de naves industriales en el Bajío", F4 "el
comité pide tres proveedores de estructura metálica en León". Inmobiliario (Inmobiliaria Cantera):
F1 "inmobiliarias confiables en Querétaro", F2 "¿conviene comprar preventa en Juriquilla?".

**Etiqueta `tipo_consulta`** en cada consulta: `informacional`, `local` o `transaccional`. La
mezcla de fuentes que cita el asistente depende del tipo (Yext vs Muck Rack, ver
`geo-evidencia.md` 2.3), así que el censo se lee por tipo.

**Regla de inmutabilidad.** El set **no se modifica** entre corridas: ni redacción, ni orden, ni
acentos. Una consulta nueva se agrega al final con su fecha de alta y la marca "sin histórico".
Una consulta que ya no sirve se marca retirada, no se borra.

Tamaño típico: 12-20 consultas. Menos no da lectura; más no se sostiene a mano.

## 2. Instrumento

**La UI de consumo es el instrumento oficial.** La API es complemento declarado (`origen: api`),
nunca sustituto. Razones:

- SparkToro/Gumshoe (ene-mar 2026) ⚠️ midió en UIs de consumo, que es lo que ven los usuarios [E].
- `oneglanse` (repo MIT): "la API no es el producto". Las respuestas por API usan otro sistema de
  búsqueda, otro prompt de sistema y otra frecuencia de búsqueda; las citas por API no son las de
  la UI (también lo reporta la guía de Gemini de suganthan.com).
- 8ight.AI (2026-10) midió por API y lo declara; por eso sus cifras de Claude se tratan como
  pendientes de replicar.

**Asistentes a priorizar en México.** StatCounter México (ago 2026): ChatGPT 75.1%, Gemini 16.7%
del uso de chatbots [E]. Orden: ChatGPT, Gemini, Google AIO y AI Mode (desde navegador, con
búsqueda normal), Claude. **Perplexity es opcional**: exige cuenta y su peso en México es bajo.

**Modo de sesión por asistente:**

| Asistente | Modo | Qué verificar |
|---|---|---|
| ChatGPT | Chat temporal | Que el encabezado indique la sesión sin personalizar |
| Gemini | Chat temporal | Que no cite la ubicación de la cuenta ("tu ciudad actual") |
| Claude | Chat incógnito con búsqueda web activada | Que haya buscado (si no, `busco: false`) |
| Google AIO / AI Mode | Navegador, ventana privada | Si AIO no aparece, se registra `aparece: false` con `notas: "no-disparo"` |
| Perplexity | Cuenta, sesión nueva | Opcional |

**Gotchas de sesión que contaminan la medición** (vistos en una ronda real, 2026):

- **El incógnito de Claude no apaga los conectores.** Si la cuenta tiene Drive, Notion, ClickUp u otros conectados, Claude puede contestar la consulta de marca desde datos privados. Apaga todos los conectores en el compositor antes de la ronda, anótalo, y vuelve a encenderlos al terminar. Una corrida que citó un conector se aparta, no se cuenta.
- **El perfil de la cuenta se filtra igual**: memoria del usuario o skills pueden hacer que el asistente "conozca" la marca. Una mención que trata a la marca como destinatario ("tu equipo en X") no es aparición.
- **AI Mode personaliza con la cuenta de Google** igual que Gemini con la ubicación. Mismo tratamiento: se marca en `notas` y se reporta aparte.
- **Gemini cambia de modelo al agotar cupo** (Pro → Flash → Flash-Lite). Verifica el selector en cada corrida y anota el modelo; corridas en otro modelo no son comparables y se repiten.
- Un asistente puede pedir permiso para leer una URL ("Allow once"); concederlo es parte del flujo del usuario real, pero se anota.

**Variable no controlada, declarada siempre.** Se corre desde una cuenta real y una IP real. La
ubicación se filtra (un asistente puede inyectar la ciudad de la cuenta), y la memoria puede no
estar del todo apagada. Se declara en el reporte; no se oculta.

**Gotchas de operación:**

- ChatGPT acepta prellenado por URL: `https://chatgpt.com/?temporary-chat=true&q=<consulta
  urlencoded>` y luego clic en enviar. Es más confiable que teclear, porque escribir por
  automatización falla con acentos y "ñ".
- Gemini y Claude: teclear la consulta; revisar que los acentos quedaron.
- Si se automatiza el navegador, lotes de **40 segundos o menos** por paso; un lote largo se agota y
  pierde la corrida.
- N=3 significa tres conversaciones nuevas, no tres "regenerar".

## 3. Qué se registra por corrida

Un archivo por corrida con la plantilla `templates/corrida.template.md`. Frontmatter:

| Campo | Contenido |
|---|---|
| `consulta` | Texto exacto, igual al de la batería |
| `familia` | F1 a F6 |
| `tipo_consulta` | informacional, local, transaccional |
| `asistente` | chatgpt, gemini, aio, ai-mode, claude, perplexity, copilot |
| `origen` | `ui` o `api` |
| `corrida` | 1, 2 o 3 |
| `fecha` | ISO con hora |
| `modo` | Modo de sesión usado |
| `busco` | `true` si el asistente mostró búsqueda o fuentes; `false` si respondió de memoria |
| `aparece` | true, false (si AIO no disparó: false y `notas: "no-disparo"`) |
| `posicion` | Lugar del cliente en la lista (vacío si no aparece) |
| `nombres` | Todos los nombres propios en orden |
| `urls_citadas` | Todas las URLs que el asistente muestra como fuente |
| `cifra_pegada` | Cualquier dato que el asistente asocia al cliente (cifra, credencial, dirección), correcto o no |
| `notas` | Criterio de selección que declara el asistente, errores, confusiones |

Debajo del frontmatter van dos secciones: `## Consulta` (el texto exacto de la batería, sin reformular) y
`## Verbatim` (la respuesta completa, sin editar). Sin verbatim no hay auditoría.

## 4. Verificación de fuentes (obligatoria)

Tow Center (mar 2025): más de 60% de respuestas con cita incorrecta y URLs inventadas [E].
Cada URL citada se abre y se clasifica: **viva / muerta / no dice lo que el asistente dijo**, y
**propia / tercero**.

`python3 scripts/verificar_fuentes.py corridas/` hace la primera pasada (status HTTP, si la página
nombra al cliente). Después, revisión humana de lo dudoso.

Trampa conocida: una ficha de directorio que da 404 o 403 al script y 200 en el navegador **no está
caída, es bloqueo anti-bot**. Verificar siempre con UA de navegador antes de reportar "muerta".

## 5. Métricas

- **Índice de Citación** = corridas donde se nombra al cliente / corridas totales, por consulta ×
  asistente. Se reporta **siempre con intervalo de Wilson al 95%**, nunca como número solo. Con
  N=3 por celda el intervalo es enorme; por eso se agrega por familia y por asistente.
- **Subtotal sin marca** (F1, F2, F4 y opcionales). F3 se reporta aparte: aparecer cuando te
  nombran no es visibilidad.
- **Primer lugar**: corridas donde el cliente es el primer nombre.
- **Tasa de disparo**: % de corridas con `busco: true`, por asistente. Explica diferencias: un
  asistente que casi no busca responde desde entrenamiento.
- **Lectura angosta vs amplia**: separar consultas de categoría angosta (técnica, caso, nicho) de
  las amplias. Lo normal es que el cliente aparezca mucho más en las angostas; ese contraste dice
  dónde invertir.
- **Censo de fuentes**: qué URL sostiene el nombre del cliente en cada corrida, si está viva, si es
  propia o de tercero. Las menciones sin cita de respaldo son comunes (25% en ChatGPT, 31% en AI
  Mode, TJ Robertson 2026-10 [E]); se cuentan aparte.
- **Cifra pegada al nombre**: dato erróneo que el asistente asocia al cliente. Es KPI de riesgo:
  se rastrea su fuente y se corrige ahí.
- No se puntúa sentimiento. Se anota el criterio con que el asistente eligió (por ejemplo, "cuántos
  procedimientos de ese tipo hace al año") porque eso dice qué publicar.

`python3 scripts/indice_citacion.py corridas/` produce la tabla por consulta × asistente con
intervalos, subtotales, primer lugar, tasa de disparo y censo de fuentes en Markdown.

**Nada de "score GEO" compuesto.** No hay pesos con respaldo para combinar estas métricas.

## 6. Control placebo (opcional)

Del repo `danishashko/geo-aeo-tracker` (MIT): por cada familia, una reformulación de la misma
pregunta con otras palabras, corrida igual. Si la reformulación mueve el índice tanto como el
cambio que hiciste en el sitio, el cambio no se puede atribuir. Útil antes de reportar una mejora.

## 7. Cadencia

| Momento | Qué |
|---|---|
| Línea base | Antes de tocar nada |
| +30 y +60 días | Tras publicar cambios |
| Después | Trimestral |
| ChatGPT y AI Mode | Mensual como mínimo: rotan 74% y 56% de citas por semana (Sistrix, abr 2026 [E]) |
| AIO | Puede ir trimestral: estable en ~la mitad de las queries |

## 8. La medición que vale más

Pedirle al cliente que pregunte a **sus propios clientes cómo llegaron**, con "asistente de IA o
ChatGPT" como opción explícita en el formulario, la recepción o el CRM. Es gratis y es lo único que
convierte el canal en dato atribuible. Pew y Reuters muestran que el clic desde IA es raro (~1-4%),
así que el canal no aparecerá en analytics aunque esté funcionando.

## 9. Cómo se reporta

- Índice por asistente y por familia con su intervalo: "ChatGPT, sin marca: 7 de 12 corridas (58%,
  IC 95% 32-81%)". Nunca "estamos en 2° lugar en ChatGPT".
- Comparación contra la línea base, con la misma batería.
- Censo de fuentes: las 5-10 URLs que más sostienen al cliente y a sus competidores.
- Cifras pegadas detectadas y su origen.
- Variable no controlada declarada.
- Siguiente acción por hallazgo: quick wins, del mes, del trimestre (ver `report-template.md`).
