# Backlinks: enfoque de auditoría

> Portado y adaptado de conceptos de `AgriciDaniel/claude-seo` (v2.2.4, MIT). Los backlinks siguen
> pesando, pero en 2026 la señal es **relevancia y autoridad ganada**, no volumen.

---

## Principio

Un enlace de un sitio relevante y con autoridad real vale más que cien de directorios basura.
Google penaliza esquemas de enlaces artificiales. La estrategia sostenible es **ganar menciones**,
no comprarlas.

## Qué auditar

1. **Perfil actual**: cuántos dominios de referencia, calidad, relevancia temática, anchor text
   (demasiado exact-match = bandera roja).
2. **Enlaces tóxicos**: dominios spam apuntando al sitio → considerar disavow solo si hay daño
   evidente.
3. **Menciones sin enlace**: marcas que te nombran sin linkear → oportunidad de recuperar el link.
4. **Backlinks de la competencia**: de dónde obtienen enlaces los competidores relevantes → mapa
   de oportunidades realistas.

## Cómo ganar enlaces

Método completo en `enlaces-por-activo.md`. En corto:

- **A quién**: a las páginas que los asistentes ya citan cuando el cliente falta (paso 8,
  `censo-a-accion.md` y `scripts/objetivos_terceros.py`), no a una lista ordenada por autoridad.
- **Con qué**: un activo hecho a mano para esa página: hoja de correcciones verificadas, aviso de
  una entrada que ya no existe con su recibo, o el diagrama que le falta hecho con su propio texto.
- **En casa**: una página de datos con fuentes enlazadas (`geo-aeo.md`), para que haya a quién
  enlazar.
- Directorios legítimos del vertical y, para local, GBP, cámaras y asociaciones.
- Pocos envíos, el cliente envía, nada sin verificar, sin pago ni intercambio de enlaces.

## Herramientas

- **Search Console → Links**: el reporte de enlaces gratuito y de la fuente (Google).
- APIs de pago (**opcional, fase futura, con tus propias keys**): DataForSEO, Ahrefs, SE Ranking ,
  el plugin claude-seo las soporta como extensiones si algún día se justifica el costo. No son
  necesarias para el core.

> No prometas "X backlinks al mes" como entregable. Prometé un perfil de enlaces limpio + una
> estrategia de contenido citable.
