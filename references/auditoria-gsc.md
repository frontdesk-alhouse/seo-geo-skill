# Auditoría con Search Console (modo `--auditar`)

> Para un sitio que ya está en producción y tiene datos: qué páginas pierden clics, cuáles están a
> un empujón de página 1, dónde dos URLs pelean la misma consulta y cuánto depende el sitio de su
> marca. Cada hallazgo sale atado a una página y a una acción.
> Script: `scripts/auditoria_gsc.py`. Formato de hallazgo y severidad: `seo-core.md` §6 y §7.

**Requisito.** Propiedad verificada en Search Console con al menos 3 meses de datos. Con menos, la
curva de CTR no tiene filas suficientes y la comparación entre periodos no dice nada.

---

## 1. Exportar

En Search Console: **Rendimiento → Resultados de búsqueda**, tipo de búsqueda **Web** (ahí cuenta
también el tráfico de AI Overviews y AI Mode, Google 2025-12-10 [O]).

| Qué | Cómo |
|---|---|
| Periodo actual | Fecha: últimos 3 meses (o un rango fijo). **Exportar → Descargar CSV**. El zip trae varias tablas; se usan `Consultas.csv` y `Páginas.csv` (`Queries.csv` y `Pages.csv` si la interfaz está en inglés) |
| Periodo previo | Mismo largo, inmediatamente anterior o el mismo periodo del año pasado si hay estacionalidad. Se exporta **aparte**, no en modo "Comparar": el script lee un periodo por carpeta |
| Consulta × página | La interfaz no exporta las dos dimensiones juntas. Opciones: la API de Search Analytics con dimensiones `query` y `page`, un conector de hoja de cálculo o Looker Studio con tabla de página y consulta, exportados a CSV con columnas de consulta, página, clics, impresiones, CTR y posición. Sin esta vista no hay análisis de canibalización |

Notas de los datos:
- La interfaz exporta un número limitado de filas por tabla; para sitios grandes, la API.
- Search Console omite consultas anonimizadas: la suma de clics por consulta queda por debajo del
  total por página. Es normal; no se "cuadra".
- El script acepta encabezados en español o inglés, CTR con `%` y coma decimal, y separador coma,
  punto y coma o tabulador.

```bash
python3 scripts/auditoria_gsc.py export-actual/ --periodo-previo export-previo/ \
    --marca "elena ruiz" "dra ruiz" --min-impresiones 50
```

`--marca` lleva los términos de marca (sin acentos ni mayúsculas importan). Sin ellos, la curva y
la canibalización mezclan consultas de marca, que tienen CTR muy alto, y el análisis (f) no corre.

## 2. El CTR esperado sale del propio sitio

Las tablas fijas de "CTR esperado por posición" que circulan (posición 1 cerca de 28 %, etc.) son
previas a AI Overviews y no sirven como vara. El CTR orgánico en consultas con AIO cayó 61 % desde
mid-2024 (Seer Interactive, sep 2025 [E] ⚠️); con resumen de IA el clic a un resultado regular baja
de 15 % a 8 % (Pew, 2025-07-22 [E]). Ver `geo-evidencia.md` 2.5 y §1.

Por eso el script calcula la **curva del sitio**: mediana de CTR por banda de posición (1, 2, 3,
4-5, 6-10, 11-20, 21+), solo con consultas sin marca y con al menos `--min-impresiones`. Una banda
con menos de 3 filas no tiene curva y no se usa. La curva compara al sitio contra sí mismo: si
toda la SERP perdió CTR, eso no es un hallazgo de la página.

## 3. Los seis análisis

| | Análisis | Regla del script | Acción típica |
|---|---|---|---|
| a | **CTR bajo para su posición** | Posición 1 a 10, CTR por debajo del 70 % de la mediana de su banda. Clics en juego = impresiones × (mediana − CTR) | Reescribir title y meta description; revisar si la SERP muestra AI Overview (si sí, la vía es que la página sea citable, `geo-aeo.md`) |
| b | **Distancia de ataque** | Posición 5 a 20 con impresiones. Clics en juego estimados contra la mediana de la banda 3 | 5-10: respuesta directa al abrir, tabla o dato propio, enlaces internos. 11-20: refresco de contenido y enlaces internos desde páginas fuertes |
| c | **Pérdida entre periodos** | Misma página (o consulta) con 5 clics o más de caída | Diagnóstico: perdió 2 posiciones o más → contenido; misma posición y CTR −20 % o más → snippet o SERP; misma posición e impresiones −20 % → demanda, no se toca la página |
| d | **Canibalización** | Consulta sin marca donde 2 o más URLs tienen al menos 15 % de sus impresiones | La URL con más clics se queda la consulta; las otras se consolidan con 301 o se reescriben para otra intención (`seo-core.md` §5) |
| e | **Páginas muertas** | Tenía 5 clics o más en el periodo previo y ahora cero | Abrir la URL: 404 o `noindex` → restaurar o redirigir; viva → buscar qué página se quedó la consulta (vuelve a d) |
| f | **Marca y sin marca** | Proporción de clics sin marca | Umbral orientativo: >60 % sano, 40-60 % medio, <40 % dependiente de la marca. Dependiente: el trabajo es contenido para consultas sin marca, no más schema |

El umbral de (f) es una regla de dedo para leer el sitio, no un estándar publicado: no se le
presenta al cliente como benchmark.

El **resumen ejecutivo** elige la acción número uno: el hallazgo de a, b, c o e con más clics en
juego. Es una estimación con la curva del sitio, no una promesa de tráfico.

## 4. De la salida al reporte

- Cada fila se convierte en un hallazgo con el formato de `seo-core.md` §7: severidad, página,
  evidencia (las cifras de la tabla), acción y responsable.
- La canibalización y las páginas muertas son severidad **media** salvo que afecten una página de
  dinero; una pérdida de posición en una página de servicio principal es **alta**.
- Se reportan como máximo 10 acciones; el resto queda en el anexo.
- Las consultas de (b) con intención de pregunta son candidatas también para la batería de
  medición (`medicion-citacion.md`), como consultas nuevas al final del set.

## 5. Límites

- Search Console da promedios por fila: una posición 7.8 puede ser 3 en móvil y 12 en escritorio.
- Una caída de CTR con posición estable puede ser una AI Overview nueva en la SERP: la consulta se
  abre en una ventana privada antes de reescribir nada.
- Los umbrales del script son constantes al inicio de `auditoria_gsc.py`; si se cambian, se dice
  en el reporte.
