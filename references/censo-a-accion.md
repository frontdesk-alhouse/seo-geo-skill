# Del censo a la acción (paso 8)

> El paso 7 dice dónde aparece el cliente y qué fuentes citan los asistentes. Este paso convierte
> ese censo en una **lista corta de páginas de terceros** donde vale la pena trabajar: las que los
> asistentes ya usan para contestar las preguntas del comprador y donde el cliente no está.
> Script: `scripts/objetivos_terceros.py`. Métodos para cada objetivo: `enlaces-por-activo.md`.

**Lo que esto es y lo que no.** Es prospección guiada por citas reales, no una campaña. Por sí
sola no produce ni una mención: produce a quién escribirle, con qué y por qué. No hay garantía de
que una página corregida mueva el índice; se mide en el siguiente ciclo con la misma batería.

---

## 1. Entrada

- Las corridas del ciclo (`templates/corrida.template.md`), en la misma carpeta que lee
  `indice_citacion.py`.
- Solo consultas **sin marca**: F1, F2, F4 y las opcionales F5, F6 y F7. F3 no entra: si te
  nombran, la página que te cita ya te conoce.
- La salida JSON de `verificar_fuentes.py` sobre esa carpeta. Una URL que nadie abrió no es
  objetivo: los asistentes inventan URLs (Tow Center, mar 2025: más de 60 % de respuestas con cita
  incorrecta [E], ver `geo-evidencia.md` 2.5).

```bash
python3 scripts/verificar_fuentes.py corridas/ --nombre "Elena Ruiz" --json > verif.json
python3 scripts/objetivos_terceros.py corridas/ --dominio-propio draelenaruiz.example.com \
    --competidores competidor-uno.example.com --nombre "Elena Ruiz" --verificacion verif.json
```

El script excluye dominios propios y de competidores (con subdominios), agrupa por URL y dominio y
ordena por **corridas sin el cliente** que citan esa URL, luego por corridas totales. Las columnas
de tipo, ángulo, contacto y prioridad salen vacías: se curan a mano.

## 2. La tabla de objetivos

Una fila por URL. Lo que da el script va marcado (s); lo demás se llena abriendo la página.

| Columna | Contenido |
|---|---|
| URL y dominio (s) | La URL tal como la citó el asistente, y su dominio |
| Tipo | `listicle`, `directorio`, `comparativa`, `foro`, `medio`, `perfil`, `guía`. Se decide con la página abierta, no por la URL |
| Consultas y asistentes (s) | Dónde pesa: ids de la batería y asistentes que la citaron |
| Corridas que la citan (s) | Cuántas corridas sin marca la usan |
| Sin cliente (s) | En cuántas de esas el cliente no apareció |
| Nombrados (s) | Nombres que dio el asistente en esas corridas. **No** es lo que lista la página |
| Competidores en la página | Los que la página nombra de verdad, comprobado al abrirla |
| ¿El cliente está? | `sí`, `no`, `de pasada`, con la cita textual si está |
| Verificación (s) | Estado de `verificar_fuentes.py`; `sin abrir` no avanza |
| Ángulo | Una frase concreta y verificable: qué le falta a esa página que el cliente puede aportar |
| Método | Hoja de correcciones, Lápida, Visual faltante o perfil (ver `enlaces-por-activo.md`) |
| Contacto | Página de contacto, autor o formulario **encontrado en el propio sitio**; si no, `sin verificar` |
| Prioridad | Alta, media o baja con el criterio de §4 |

## 3. Por qué la cola y no la autoridad de dominio

- La autoridad de dominio explica poco de quién aparece: en AIO, menciones web de marca
  correlacionan 0.664 con visibilidad y DR solo 0.326 (Ahrefs, 2025-05-26, 75,000 marcas [E]).
- Los asistentes citan mucho fuera del top 10 de Google: solo 2-5 % de páginas citadas vienen del
  top 10 (TJ Robertson, 2026-10-25 [E]); solo 38 % de citas de AIO rankean top 10 (Ahrefs,
  2026-03-02 [E]).
- 93 % de los dominios citados en búsquedas locales son sitios de negocios individuales
  (BrightLocal, 2026-08-26 [E]).
- Lectura nuestra [S]: en la cabeza (Wikipedia, Reddit, YouTube, LinkedIn, medios grandes) DR y
  cita coinciden y nadie entra este trimestre por un correo. La diferencia está en la cola: blogs
  de nicho, directorios del vertical, asociaciones, comparativas chicas. Ahí un editor contesta y
  ahí ordenar por DR esconde lo que los asistentes de verdad leen.

La cabeza no se borra del censo: se reporta. Solo sale de la lista de outreach. Reddit, YouTube o
LinkedIn se trabajan con participación real del cliente, nunca con campañas pagadas.

## 4. Prioridad

| Prioridad | Criterio |
|---|---|
| Alta | Citada en 2 o más consultas sin el cliente, o por 2 o más asistentes; viva; ángulo verificable; contacto verificado |
| Media | Una consulta o un asistente; ángulo verificable; contacto verificado o formulario público |
| Baja | Ángulo débil o sin contacto verificado. Se deja en el censo y se revisa en el siguiente ciclo |

Una lista útil tiene de 5 a 20 filas. Si salen 80, el ángulo no se escribió con la página abierta.

## 5. Reglas

1. **Nada inventado.** Ni URLs, ni competidores en la página, ni contactos, ni cifras. Si no se
   pudo abrir o comprobar, la celda dice `sin verificar` y la fila no sube de prioridad baja.
2. **La fuente se abrió.** `verificar_fuentes.py` primero; `bloqueo-anti-bot` se abre en un
   navegador real antes de descartarla.
3. **El cliente envía; el agente solo redacta.** Borrador listo para pegar, desde el correo del
   cliente. Nunca se afirma que algo se envió si no lo envió el cliente.
4. **Una mención sin enlace también cuenta.** Las menciones correlacionan más que los backlinks
   (Ahrefs 2025-05-26 [E]); que el editor agregue el nombre sin enlace no es un fracaso.
5. **Sin pago.** Pagar por entrar a una lista de "los mejores" está en anti-patrones; si un editor
   pide dinero, la fila se cierra.

## 6. Cierre del ciclo

En el reporte (`templates/reporte-geo.template.md`, sección de objetivos): la tabla curada, qué se
envió y qué contestaron. En el siguiente ciclo se corre la misma batería: si una página trabajada
empieza a nombrar al cliente, el censo lo muestra con la URL. No se atribuye causalidad: se
reporta la coincidencia y la fecha del cambio.
