# Analytics de IA: qué se puede ver gratis y qué no

> GA4, Bing Webmaster Tools, Search Console, IndexNow y Webflow AEO. Etiquetas como en
> `geo-evidencia.md`.

**Antes de configurar nada, fijar la expectativa.** El clic desde IA es raro: ~1% en enlaces de
resúmenes de Google (Pew, 2025-07-22) y ~4% desde chatbots (Reuters DNR 2026) [E]. Analytics ve
la punta del canal, no el canal. El KPI sigue siendo cita y mención (`medicion-citacion.md`);
analytics es la evidencia secundaria de que esas citas mandan visitas.

---

## 1. GA4: canal de referidos IA

Por defecto GA4 mete chatgpt.com, perplexity.ai y similares en **Referral**, mezclados con todo lo
demás. Se crea un grupo de canales personalizado.

**Pasos:**

1. Admin → Data display → Channel groups → Create new channel group (copia del predeterminado).
2. Add new channel → nombre `Asistentes IA`.
3. Condición: **Source** · matches regex · pegar:

```
(^|\.)(chatgpt\.com|chat\.openai\.com|perplexity\.ai|gemini\.google\.com|bard\.google\.com|copilot\.microsoft\.com|edgeservices\.bing\.com|claude\.ai|deepseek\.com|grok\.com|meta\.ai)$
```

4. **Reordenar: `Asistentes IA` por encima de Referral.** GA4 asigna el primer canal que coincide;
   si queda debajo, nunca recibe nada.
5. Guardar y usarlo como dimensión primaria en Acquisition → Traffic acquisition. Aplica también a
   datos históricos (los grupos personalizados reprocesan).

**Notas:**

- GA4 habría lanzado un canal nativo "AI Assistant" (2026-05-13) que excluye Perplexity ⚠️
  cobertura secundaria. Si aparece en la propiedad, conservar el personalizado igual: cubre más
  fuentes y es comparable con meses anteriores.
- ChatGPT agrega `utm_source=chatgpt.com` a muchos enlaces que pone en sus respuestas. Revisar
  también Session source / medium con ese valor.
- **Mucho tráfico de IA llega como Direct**: apps de escritorio y móvil, copiar y pegar la URL,
  navegadores con IA. No hay forma de recuperarlo; se declara.
- Los clics desde AIO y AI Mode caen en **Organic Search**, indistinguibles del orgánico normal.
- Crear una exploración con landing page × canal `Asistentes IA` para ver qué páginas reciben ese
  tráfico. Suele coincidir con las URLs del censo de fuentes.
- Si el cliente tiene CRM, guardar el `source` de la primera visita en el lead para ligar IA a
  conversiones reales.

## 2. Bing Webmaster Tools: AI Performance

**Único reporte gratuito de citas de primera parte** [O]. Preview público desde feb 2026 en
bing.com/webmasters/aiperformance: muestra cuántas veces Copilot y las respuestas de IA de Bing
citaron cada página del sitio y con qué consultas de grounding. Sin clics.
https://searchengineland.com/bing-webmaster-tools-testing-new-ai-performance-report-468039

**Cómo activarlo:**

1. Entrar a Bing Webmaster Tools con una cuenta Microsoft.
2. Agregar el sitio. Lo más rápido: **importar desde Google Search Console** (trae propiedad y
   sitemaps). Alternativa: verificación por meta tag (Webflow: Site Settings → Custom code → Head;
   Framer: Site Settings → General → Custom Code) o registro DNS.
3. Enviar el sitemap si no se importó.
4. AI Performance se llena con el tiempo; revisarlo a las 2-4 semanas.

Lectura: las consultas de grounding dicen qué preguntas está contestando Copilot con tus páginas.
Sirven para alimentar la batería de medición (como consultas nuevas al final, con fecha de alta).

**Bing como seguro barato.** Bing y Copilot comparten índice [O]. La relación ChatGPT y Bing está
en disputa: OpenAI tiene índice propio (OAI-SearchBot), Seer reportó que 87% de citas de ChatGPT
coincidían con el top de Bing, y pruebas de 2026 sugieren un giro hacia Google [S]. Estar bien
indexado en Bing cuesta una hora y cubre ese escenario.

## 3. Search Console: reporte Generative AI

Beta desde 2026-06-03 [O]: **solo impresiones**, AIO + AI Mode + Discover combinados, sin clics y
sin desglose por superficie. El tráfico de AIO y AI Mode también cuenta dentro del tipo de
búsqueda "Web" del reporte de rendimiento normal.

Sirve para: ver si las páginas clave aparecen en superficies de IA de Google y su tendencia. No
sirve para: atribuir clics ni separar AIO de AI Mode. No se reporta como "citas".

## 4. IndexNow

Protocolo para avisar a Bing (y Yandex, Seznam, Naver) que una URL cambió [O]. Bing reporta que
~50% de las URLs nuevas clicadas en su buscador llegan por IndexNow. Google no participa.

- Webflow y Framer: sin soporte nativo confirmado. Opciones: enviar manualmente desde Bing
  Webmaster Tools (URL Submission) al publicar páginas clave, o un webhook de publicación de
  Webflow que llame a la API de IndexNow (requiere un servicio intermedio y la key en la raíz).
- Para la mayoría de sitios de estudio basta el envío manual en cada lanzamiento o cambio grande.

## 5. Webflow AEO

Anunciado 2026-04-13, disponible para Enterprise desde 2026-05-21 [O vía prensa]. Incluye analítica
de visitas de bots de IA, citas de marca, conversiones atribuidas a IA y Prompt Insights (ChatGPT
primero); agentes de contenido desde 2026-07-28; consume créditos de IA desde 2026-06-29. Requiere
Analyze for Enterprise. En el MCP de Webflow su superficie es `data_aeo_tool`.

Cuándo aplica: solo si el cliente ya está en Enterprise. La mayoría de clientes de estudio no lo
están; para ellos, el stack manual de este archivo. Si está disponible, sus datos de prompts se
tratan como [S vendor] hasta contrastarlos con la medición propia, y los bots de IA que registra
sirven para confirmar que robots.txt y Cloudflare no los están frenando.

## 6. Herramientas pagas

| Herramienta | Qué hace | Para quién |
|---|---|---|
| Profound | Monitoreo de citas a escala, multi-asistente | Enterprise |
| Peec AI | Seguimiento de prompts y citas por marca | Agencias, mediano |
| Otterly | Seguimiento de prompts de bajo costo | Pyme, agencia chica |
| Semrush AI Toolkit | Visibilidad IA dentro de Semrush | Si ya pagan Semrush |
| Ahrefs Brand Radar | Menciones de marca en IA, con YouTube y Reddit desde ene 2026 | Si ya pagan Ahrefs |

Todas miden en su mayoría por API o con su propio muestreo; sus cifras no son comparables con la
medición manual en UI. Si el cliente paga una, se usa como complemento declarado, no como
reemplazo del protocolo. Ninguna convierte su "score" en evidencia de causa.

## 7. El reporte mensual

| Bloque | Fuente | Qué se escribe |
|---|---|---|
| Citas medidas | Corridas manuales + `scripts/indice_citacion.py` | Índice por asistente y familia con intervalo; solo en meses de medición |
| Citas en Bing/Copilot | Bing WMT AI Performance | Páginas más citadas y consultas de grounding nuevas |
| Presencia en Google IA | Search Console Generative AI | Tendencia de impresiones de páginas clave |
| Visitas desde IA | GA4 canal `Asistentes IA` | Sesiones, landing pages, conversiones; comparar con mes anterior |
| Atribución declarada | Pregunta "¿cómo nos conociste?" | Conteo de respuestas "asistente de IA" |
| Salud técnica | `scripts/check_html_crudo.py` | Bots sin bloqueo, HTML crudo correcto, llms.txt y sitemap vivos |

Reglas: no sumar estas fuentes en un número único; cada una mide una cosa distinta. Declarar
siempre que Direct esconde parte del canal. Ver `report-template.md` para el formato al cliente.
