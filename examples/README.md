# Ejemplos

Material ficticio para probar los scripts sin tocar datos de un cliente real. Todos los comandos se corren desde la raíz del skill (la carpeta que contiene `scripts/`). Requisito: Python 3.10 o superior, sin dependencias externas.

## Qué hay aquí

- `corridas-ejemplo/`: 12 corridas de una clienta ficticia, la Dra. Elena Ruiz (cirugía de columna, Monterrey), escritas con `templates/corrida.template.md`.
  - Q-01 (F1, local): 3 corridas en ChatGPT y 3 en Gemini.
  - Q-02 (F2, informacional): 3 corridas en ChatGPT; una con `busco: false` (respondió sin buscar).
  - Q-03 (F3, con marca): 3 corridas en ChatGPT; una con `cifra_pegada`.
  - Competidores y URLs son inventados y viven en `example.com` y `example.org`.
- `urls-ejemplo.txt`: 5 URLs públicas y estables (una fuerza un 404) para probar `verificar_fuentes.py`.
- `gsc-ejemplo/`: exportaciones ficticias de Search Console del sitio de la misma clienta. `actual/` trae consultas, páginas y la vista consulta × página con encabezados en español (coma decimal, CTR con `%`); `previo/` trae páginas y consultas del periodo anterior con encabezados en inglés.

## Cómo correr cada script

**Índice de Citación** (sin red):

```bash
python3 scripts/indice_citacion.py examples/corridas-ejemplo
python3 scripts/indice_citacion.py examples/corridas-ejemplo --json | python3 -m json.tool | head -40
```

Qué esperar: Q-01 en 4/6, Q-02 en 1/3, Q-03 (marca) aparte en 3/3; subtotal sin marca 5/9 con intervalo de Wilson [27-81 %]; tasa de disparo de ChatGPT 8/9; una cifra pegada; una advertencia porque Gemini solo corrió Q-01.

**Verificar fuentes** (con red):

```bash
python3 scripts/verificar_fuentes.py examples/urls-ejemplo.txt --nombre "Example"
python3 scripts/verificar_fuentes.py examples/urls-ejemplo.txt --nombre "Example" --ua ambos
```

Las URLs de `corridas-ejemplo/` son ficticias: si corres el script sobre esa carpeta, casi todas saldrán `muerta`, que es justo lo que verías con una URL inventada por un asistente.

**HTML crudo por bot, robots.txt y llms.txt** (con red; usa un sitio tuyo o de un cliente con permiso):

```bash
python3 scripts/check_html_crudo.py https://www.tu-sitio.mx --textos "frase clave del hero" "{{CIUDAD}}"
python3 scripts/check_html_crudo.py https://www.tu-sitio.mx --bots GPTBot,OAI-SearchBot --json
```

**Metadata publicada** (con red):

```bash
python3 scripts/verificar_metadata.py https://www.tu-sitio.mx/sitemap.xml
python3 scripts/verificar_metadata.py https://www.tu-sitio.mx/contacto
```

**Borrador de llms.txt** (con red):

```bash
python3 scripts/generar_llms_txt.py https://www.tu-sitio.mx/sitemap.xml --max 30
python3 scripts/generar_llms_txt.py tu-sitio.mx --secciones "Servicios:/servicios,/precios" "Sobre:/nosotros,/contacto" --salida llms-borrador.txt
```

El borrador sale con `TODO` en el resumen, el contexto y las Notas para modelos de lenguaje. Se cura a mano con `templates/llms.txt.template` como guía antes de publicarlo.

**Objetivos de terceros, paso 8** (sin red):

```bash
python3 scripts/objetivos_terceros.py examples/corridas-ejemplo --dominio-propio draelenaruiz.example.com --nombre "Elena Ruiz"
python3 scripts/objetivos_terceros.py examples/corridas-ejemplo --competidores competidor-uno.example.com --json
```

Qué esperar: 9 corridas sin marca, 4 sin la clienta; la página del competidor uno arriba (6 corridas, 3 sin la clienta) si no la excluyes; la columna de verificación en `sin abrir` y una advertencia, porque no se pasó `--verificacion`.

**Auditoría de Search Console** (sin red):

```bash
python3 scripts/auditoria_gsc.py examples/gsc-ejemplo/actual --periodo-previo examples/gsc-ejemplo/previo --marca "elena ruiz" "dra ruiz"
python3 scripts/auditoria_gsc.py examples/gsc-ejemplo/actual/consulta-pagina.csv --json
```

Qué esperar: curva con 3 filas por banda de la 1 a la 11-20; acción número uno "hernia de disco lumbar" en `/hernia-de-disco` (posición 7.8, 66 clics en juego); dos canibalizaciones; una página muerta (`/blog/ciatica-ejercicios`); pérdidas con diagnóstico de CTR y de posición; 48.9 % de clics sin marca (medio).

## Códigos de salida

| Script | 0 | 1 |
|---|---|---|
| `indice_citacion.py` | reporte generado | carpeta inexistente o ninguna corrida válida |
| `verificar_fuentes.py` | reporte generado | sin URLs, archivo inexistente o ninguna URL respondió |
| `check_html_crudo.py` | sin hallazgos ERROR | algún ERROR (bot de búsqueda bloqueado, texto clave ausente, noindex) o sitio sin respuesta |
| `verificar_metadata.py` | sin problemas ERROR | algún ERROR (title o description ausente, sin h1, noindex, status distinto de 200) |
| `generar_llms_txt.py` | borrador generado | sitemap ilegible o sin URLs |
| `objetivos_terceros.py` | lista generada | carpeta inexistente, ninguna corrida válida o sin corridas sin marca |
| `auditoria_gsc.py` | auditoría generada | ruta inexistente, sin CSV o ningún CSV con columnas de Search Console |
