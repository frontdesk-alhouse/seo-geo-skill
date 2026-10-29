## Visibilidad en asistentes de IA: {{MES AAAA}}

Ciclo {{n}} · corridas del {{AAAA-MM-DD}} al {{AAAA-MM-DD}} · {{N}} corridas en {{asistentes}} · comparado contra el ciclo del {{AAAA-MM-DD}}.

Las cifras salen de `scripts/indice_citacion.py` y `scripts/verificar_fuentes.py`; el método está en `references/medicion-citacion.md`.

### Lo importante en tres líneas

1. {{Dónde estamos: subtotal sin marca y su intervalo, en una frase.}}
2. {{Qué cambió contra el ciclo anterior y si el cambio sale del intervalo o no.}}
3. {{La acción con más impacto para el mes que entra.}}

### Índice de Citación por consulta y asistente

Celdas `k/n (posiciones)`: en cuántas de n corridas te nombraron y en qué lugar. La consulta de marca va aparte.

| Consulta | Familia | Tipo | ChatGPT | Gemini | Claude | AI Overviews | AI Mode | Total |
|---|---|---|---|---|---|---|---|---|
| Q-01 {{texto corto}} | F1 | local | {{2/3 (2, 3)}} | | | | | {{k/n · % [lo-hi %]}} |
| Q-02 {{texto corto}} | F2 | informacional | | | | | | |
| Q-05 {{texto corto}} (marca) | F3 | informacional | | | | | | |

**Subtotal sin marca**

| Asistente | Te nombra | Primer lugar | Buscó en la web (tasa de disparo) |
|---|---|---|---|
| ChatGPT | {{k/n · % [lo-hi %]}} | {{k/n}} | {{k/n}} |
| Gemini | | | |
| Claude | | | |
| Global | | | |

Entre corchetes va el intervalo de Wilson al 95 %. Dos ciclos cuyos intervalos se traslapan no muestran un cambio real, aunque el porcentaje se mueva.

**Lectura por tipo de consulta (sin marca):** informacional {{k/n}}, local {{k/n}}, transaccional {{k/n}}. {{Una frase: dónde se gana y dónde no.}}

### Censo de fuentes

Qué páginas sostienen lo que los asistentes dicen de ti y de tu competencia.

| URL | Corridas que la citan | ¿Te nombra? | Estado | Propia o tercero | Qué dice de ti |
|---|---|---|---|---|---|
| {{https://...}} | {{n}} | {{sí/no}} | {{viva / muerta / bloqueo anti-bot}} | {{propia / tercero}} | {{resumen en una línea, o "no te menciona"}} |

{{Una frase: qué fuente de tercero vale más mantener viva y cuál conviene corregir o reemplazar.}}

### Cifras pegadas al nombre

Datos erróneos o no publicados que algún asistente asocia contigo. Son riesgo de reputación: se rastrean hasta su fuente y se corrigen en el origen.

| Cifra o dato | Consulta | Asistente | Corridas | Fuente probable | Acción |
|---|---|---|---|---|---|
| {{"más de N ..."}} | {{Q-05}} | {{chatgpt}} | {{1/3}} | {{perfil de directorio}} | {{corregir el perfil; volver a medir}} |

### Cambios contra el ciclo anterior

| Métrica | Ciclo anterior | Este ciclo | ¿Fuera del intervalo? |
|---|---|---|---|
| Sin marca, global | | | {{sí/no}} |
| Sin marca, ChatGPT | | | |
| Sin marca, Gemini | | | |
| Primer lugar, global | | | |
| Fuentes propias citadas | | | |
| Cifras pegadas activas | | | |

{{Qué se publicó o cambió entre ciclos: páginas nuevas, perfiles corregidos, reseñas, menciones. Sin afirmar causalidad.}}

### Plan

**Quick wins (esta semana)**

- [ ] {{Acción concreta, responsable, fecha.}}
- [ ] {{Acción concreta, responsable, fecha.}}

**Este mes**

- [ ] {{Acción, responsable, fecha.}}

**Este trimestre**

- [ ] {{Acción, responsable, fecha.}}

Siguiente medición: {{AAAA-MM-DD}} (30 y 60 días después de publicar cambios; después, trimestral).

### Cómo leer estas cifras (método)

Los asistentes de IA no tienen un ranking fijo: la misma pregunta hecha dos veces devuelve listas distintas. Por eso no reportamos una posición sino una proporción: en cuántas de varias corridas te nombran, con su intervalo de confianza. Hicimos {{N}} corridas por consulta y asistente con sesiones reales en modo temporal o incógnito, desde {{país}}; la ubicación y la cuenta son variables que no controlamos, así que estas cifras sirven para comparar contra nuestras propias mediciones anteriores, no como verdad absoluta. El set de consultas no cambia entre ciclos. No hay forma de garantizar que un asistente te cite: lo que sí podemos es mejorar lo que las fuentes dicen de ti y medir si eso se refleja. El indicador es la mención y la cita, no el tráfico: muy poca gente da clic a las fuentes de una respuesta.
