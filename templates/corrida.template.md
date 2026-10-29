---
# Id de la consulta en la batería (Q-01, Q-02...). Nunca se reutiliza un id.
consulta: Q-01
# Familia: F1 sin marca por necesidad, F2 sin marca por decisión, F3 con marca, F4 tercero, F5 caso específico, F6 técnica.
familia: F1
# Tipo de consulta: informacional | local | transaccional (se copia de la batería, no se decide por corrida).
tipo_consulta: local
# Asistente: chatgpt | gemini | claude | perplexity | aio | aimode | copilot
asistente: chatgpt
# Origen: ui (interfaz de consumo, instrumento oficial) | api (solo como complemento declarado).
origen: ui
# Número de corrida para esta consulta y asistente: 1..N (N=3 por defecto).
corrida: 1
# Fecha de la corrida en ISO (AAAA-MM-DD). Si quieres la hora, anótala en notas.
fecha: 2026-01-15
# Modo de sesión en texto libre: temporal-unpersonalized, chat-temporal, incognito, sesion-iniciada...
modo: temporal-unpersonalized
# busco: true si el asistente ejecutó búsqueda web (muestra fuentes o "buscando"); false si respondió de memoria.
busco: true
# aparece: true si el cliente es nombrado en la respuesta (aunque sea de pasada).
aparece: false
# posicion: lugar del cliente en el orden de nombres (1 = primero). null si no aparece o no hay orden.
posicion: null
# nombres: todos los negocios o personas nombrados, en el orden en que aparecen. Lista [a, b] o con guiones.
nombres: []
# urls_citadas: cada URL que el asistente mostró como fuente, tal cual. Después se verifican con verificar_fuentes.py.
urls_citadas: []
# cifra_pegada: dato erróneo o no publicado que el asistente asocia al cliente (entre comillas). null si no hay.
cifra_pegada: null
# notas: criterio de selección que declaró el asistente, errores, fugas de ubicación, incidentes. Entre comillas.
notas: ""
---

## Consulta

Texto exacto de la consulta, copiado de la batería. No se reformula.

## Verbatim

Pega aquí la respuesta completa, sin editar, incluidas las listas y el texto de las fuentes.
