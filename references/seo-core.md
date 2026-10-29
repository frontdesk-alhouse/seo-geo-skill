# SEO técnico base: checklist, tipos de página, fórmulas y severidad

> El piso de cualquier sitio antes de hablar de schema o de GEO. Si esto está roto, nada de lo
> demás importa: un asistente de IA no cita lo que el buscador no puede rastrear ni indexar.

Principios:
1. Bloqueos técnicos primero, contenido después.
2. Una página, una intención de búsqueda principal.
3. Señales de calidad de largo plazo; nada de trucos.
4. Indexación mobile-first: se revisa en móvil.
5. Cada recomendación apunta a una página o asset concreto y se puede implementar.

---

## 1. Checklist técnico

### Rastreo
- [ ] `robots.txt` deja pasar las páginas importantes y bloquea solo superficies de poco valor
      (búsquedas internas, parámetros, carritos).
- [ ] `robots.txt` no bloquea bots de búsqueda de IA (ver `ai-crawlers.md`).
- [ ] Ninguna página clave queda a más de 3 clics de la home.
- [ ] Redirects: **2 saltos máximo** de la URL vieja a la final; sin bucles.
- [ ] Sin enlaces internos rotos en rutas clave.

### Indexación
- [ ] Ninguna página importante en `noindex` por accidente (meta robots y header `X-Robots-Tag`).
- [ ] Formato de URL único y consistente (con o sin `www`, con o sin barra final, siempre igual).
- [ ] Canonical presente, absoluto, apuntando a producción, autoconsistente y sin bucles.
- [ ] Sin URLs duplicadas compitiendo sin control de canonical.
- [ ] Sitemap XML refleja la superficie pública real y está enviado en Search Console y Bing.
- [ ] Sitio multilingüe: `hreflang` recíproco en cada versión, con `x-default`.
- [ ] Staging sin indexar.

### Rendimiento (Core Web Vitals, percentil 75 de campo)
| Métrica | Bueno | Arreglos típicos |
|---|---|---|
| LCP | < 2.5 s | Precargar la imagen del hero, quitar trabajo que bloquea el render |
| INP | < 200 ms | Recortar JS pesado, partir tareas largas |
| CLS | < 0.1 | Dimensiones explícitas en imágenes y embeds, reservar espacio |

Los datos de campo (Search Console, CrUX) mandan sobre Lighthouse local, que varía mucho entre
corridas.

### Estructura on-page
- [ ] Un solo `H1`, que dice de qué trata la página.
- [ ] `H2` y `H3` reflejan la jerarquía real del contenido, no el tamaño visual que se quería.
- [ ] Texto alternativo descriptivo en imágenes con contenido.
- [ ] El copy clave está en el HTML servido, no inyectado por JS (ver `ai-crawlers.md`).

---

## 2. Tipo de página → schema.org

| Tipo de página | Schema | Nota |
|---|---|---|
| Home | `Organization` o subtipo de `LocalBusiness` + `WebSite` | Un solo `@id` de organización en todo el sitio |
| Interior | `BreadcrumbList` | Refleja la ruta real de navegación |
| Servicio | `Service` con `provider` al `@id` de la organización | |
| Producto físico | `Product` + `Offer` | Precio y disponibilidad solo si están visibles |
| Software | `SoftwareApplication` | `Offer` solo con precio publicado |
| Artículo, blog | `Article` / `BlogPosting` con `datePublished` y `dateModified` | Fechas iguales a las visibles |
| Persona (médico, fundador, autor) | `Person` con `sameAs` verificados | Ver `entidad-sameas.md` |
| Contacto, ubicación | `LocalBusiness` con NAP idéntico al perfil de Google | Ver `local-seo.md` |
| Preguntas frecuentes | `FAQPage` solo si la página **es** preguntas y respuestas visibles | Sin rich result desde 2026-05-07 |
| Término propio | `DefinedTerm` | Útil para que una postura nombrable tenga entidad |

---

## 3. Fórmulas de title y meta

**Title** (50 a 60 caracteres, concepto al frente, legible por una persona):

```text
Tema principal + modificador concreto | Marca
```
Ejemplos: `Cirugía de columna mínimamente invasiva en Monterrey | Clínica Ejemplo` ·
`Software de inventario para ferreterías | Ejemplo App`.

**Meta description** (120 a 160 caracteres, honesta, sin promesas):

```text
Qué haces + para quién + un dato concreto que lo respalda + siguiente paso
```

Reglas: únicos por página; nada de nombre de marca repetido como title; sin listas de keywords;
en plantillas CMS, bindeados a campos del item.

---

## 4. Enlaces internos y anchors

- Enlaza desde las páginas fuertes (home, servicios principales) hacia las que quieres posicionar.
- Anchor descriptivo: "cirugía de hernia de disco", no "ver más" ni "clic aquí".
- Cada página nueva recibe al menos 2 enlaces desde páginas existentes relevantes y da al menos
  uno de vuelta.
- Páginas huérfanas (sin enlaces entrantes) se enlazan o se retiran.

---

## 5. Mapa keyword → página

1. Define la intención: informacional, comercial o transaccional.
2. Junta variantes reales (autocompletado, Search Console, preguntas de clientes).
3. Prioriza por coincidencia de intención, valor probable y competencia.
4. **Un clúster por página**: una keyword principal y sus variantes cercanas viven en una sola
   URL.
5. Detecta canibalización: si dos URLs pelean el mismo clúster, consolida o diferencia.

| Clúster | Intención | URL | Keyword principal | Variantes |
|---|---|---|---|---|

---

## 6. Taxonomía de severidad

| Nivel | Qué es | Ejemplos |
|---|---|---|
| **Crítico** | Impide rastrear, indexar o citar páginas importantes. Se arregla antes de publicar | `noindex` en la home; `robots.txt` bloquea `/` o bloquea `OAI-SearchBot`; canonical en bucle o hacia staging; cadena de 3 o más redirects; staging indexado; copy clave solo existe tras ejecutar JS |
| **Alto** | Daña relevancia o elegibilidad en páginas clave | Titles o metas faltantes o duplicados; varios `H1`; JSON-LD inválido o ausente en tipos clave; schema que marca contenido no visible; CWV en rojo en páginas importantes; `sameAs` hacia perfiles inexistentes |
| **Medio** | Debilita, pero no bloquea | Contenido delgado; alt faltante; anchors genéricos; páginas huérfanas; canibalización; sin fecha visible de actualización en páginas clave |
| **Bajo** | Pulido | Title algo largo; OG sin imagen propia en páginas secundarias; descripciones mejorables |

## 7. Formato de hallazgo

```text
[ALTO] Titles duplicados en las páginas de servicio
Página: /servicios/* (12 URLs)
Evidencia: las 12 devuelven "Servicios | Marca" en el HTML servido (verificar_metadata.py, 2026-10-28)
Por qué importa: el buscador no distingue qué página responde a qué intención
Fix: title por plantilla = "{{nombre del servicio}} en {{ciudad}} | Marca"
```

Reglas del hallazgo: siempre página o URL concreta, evidencia reproducible (comando, captura o
fragmento del HTML servido, con fecha) y un fix que quien lo recibe puede implementar sin
preguntar. Nada de folclor SEO ni patrones manipulativos.
