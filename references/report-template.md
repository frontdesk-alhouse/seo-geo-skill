# Reporte SEO + GEO para cliente: plantilla

> Concepto de estructura adaptado de `AgriciDaniel/claude-seo` (MIT). Forma del entregable que se
> le presenta al cliente. Honesto, accionable, sin jerga vacía.

---

## Estructura

### 1. Resumen ejecutivo (media página)
- Estado general en una frase.
- 3 hallazgos más importantes.
- Qué se hizo / qué falta.
- Recordatorio honesto: schema y SEO técnico = visibilidad, CTR y comprensión de entidad; el
  tráfico lo mueven contenido, autoridad e intención; en asistentes de IA se mide la cita, no se
  promete.

### 2. SEO técnico
| Ítem | Estado | Acción |
|---|---|---|
| Rastreo / robots.txt | ✅/⚠️/❌ | |
| Indexación (noindex accidental, staging) | | |
| Canonicals | | |
| Sitemap XML | | |
| Core Web Vitals (LCP/INP/CLS) | | |
| HTTPS / redirects | | |

### 3. Schema markup
| Página / tipo | Schema aplicado | Validado (Rich Results / validator) | Detectado en Search Console |
|---|---|---|---|
| Home: Organization/WebSite | | | |
| Interiores: BreadcrumbList | | | |
| {{vertical}} | | | |

### 4. On-page
- Titles y metas únicos y en rango.
- Jerarquía de headings.
- Alt text de imágenes.
- Enlaces internos.

### 5. Contenido / E-E-A-T
- Autoría y señales de autoridad verificables (crítico en médico).
- Superficie citable: respuesta directa, tablas, fechas visibles, precios (ver `geo-aeo.md`).

### 6. Local (si aplica)
- NAP consistente, perfil de Google verificado, reseñas.

### 7. Visibilidad en asistentes de IA
El detalle va en `templates/reporte-geo.template.md`; aquí se resume:

- Índice de Citación sin marca por asistente, **como rango** (con intervalo), contra la línea base.
- Consultas de marca aparte: ¿lo describen bien? ¿hay una cifra o dato erróneo pegado al nombre?
- Censo de fuentes: qué URLs sostienen la mención, cuáles son propias y cuáles de terceros,
  cuáles están vivas.
- Estado técnico GEO: bots de búsqueda permitidos, copy en HTML crudo, `sameAs` vivos.
- Nunca "posición en ChatGPT"; nunca un score compuesto.

### 8. Plan priorizado
| Horizonte | Acciones (cada una atada a una página, perfil o asset) |
|---|---|
| **Quick wins** (esta semana) | Bloqueos críticos, robots, metadata faltante, `sameAs` rotos, fechas visibles |
| **Este mes** | Respuesta directa y tablas en páginas clave, perfiles de terceros corregidos, schema del vertical |
| **Este trimestre** | Contenido de experiencia propia, menciones ganadas en fuentes que el censo mostró, nueva medición |

---

## Métricas a reportar (con fuente honesta)

| Métrica | Fuente |
|---|---|
| Impresiones, clics, CTR, posición promedio | **Search Console** (dato duro de Google) |
| Impresiones en funciones de IA (AIO, AI Mode y Discover combinados; sin clics) | **Search Console**, reporte Generative AI |
| Citas en Copilot y Bing por página y consulta | **Bing Webmaster Tools**, AI Performance |
| Sesiones referidas por asistentes | **GA4**, canal de IA personalizado (ver `analytics-ia.md`) |
| Índice de Citación y censo de fuentes | Medición propia (`medicion-citacion.md`, `scripts/indice_citacion.py`) |
| Páginas indexadas, rich results válidos o con error | Search Console |
| Core Web Vitals | Search Console / PageSpeed Insights |

> Cifras de la industria (por ejemplo, lifts por agregar tablas) se presentan como **estimaciones
> de estudios correlacionales**, con fuente y fecha, nunca como garantía. Los números del propio
> cliente son la verdad.
