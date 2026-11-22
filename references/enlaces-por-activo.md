# Enlaces por activo: ganar menciones con algo hecho a mano

> Cómo conseguir que una página de tercero nombre o enlace al cliente sin comprar nada: llevarle al
> editor algo que mejora su página y que le costaría trabajo hacer. Pocos envíos, cada uno con un
> activo real. La lista de a quién escribirle sale del paso 8 (`censo-a-accion.md`).

**Encuadre.** Un enlace o una mención en una página que los asistentes ya citan es superficie de
tercero viva, la palanca de Tier 2-3 de `geo-evidencia.md` §7. Las menciones de marca
correlacionan más con visibilidad en AIO que los backlinks (0.664 contra 0.218, Ahrefs
2025-05-26 [E]): una mención sin enlace cuenta como resultado. Nada de esto es interruptor; se
mide en el siguiente ciclo.

---

## Reglas comunes (valen para los tres métodos)

1. **Ninguna afirmación sobre la página ajena sin verificar.** Los tres métodos funcionan
   diciéndole al editor algo sobre su propio contenido. Su primer gesto es comprobarlo; un solo
   error y el cliente queda como spam. Lo que no se pudo confirmar contra una fuente primaria sale
   de la lista; no se suaviza con "parece que".
2. **Pocos envíos trabajados.** De 5 a 20 por ciclo, cada uno con su activo. El método deja de
   funcionar en volumen porque lo que convence es que se nota hecho a mano. Si piden escalarlo a
   cientos, se dice que no.
3. **El cliente envía.** El agente prepara el activo y el borrador; el cliente lo manda desde su
   correo y con su nombre. Nunca se afirma que algo se envió.
4. **Sin pago y sin intercambio.** Ni dinero, ni "te enlazo si me enlazas". El intercambio
   excesivo de enlaces y las páginas de socios solo para enlazarse son spam de enlaces según
   Google ("Spam policies for Google web search", consultada 2026-11-22 [O]).
5. **Honestidad sobre el reemplazo.** Si el cliente no es la mejor alternativa para un hueco, se
   dice quién lo es. Un editor que te pesca exagerando una vez no abre el siguiente correo.

## El generador de la lista: paso 8

`scripts/objetivos_terceros.py` ordena las páginas que los asistentes citan cuando el cliente
falta. A cada fila curada se le asigna uno de los métodos de abajo según lo que la página es:

| La página es | Método |
|---|---|
| Lista o comparativa que incluye a alguien que ya no existe o cambió de giro | Lápida |
| Guía o artículo con cifras, precios, fechas o "actualmente" | Hoja de correcciones |
| Guía larga que describe un proceso, una comparación o una jerarquía sin diagrama | Visual faltante |
| Directorio o perfil del vertical | Alta o corrección del perfil (`entidad-sameas.md`) |

## 1. Hoja de correcciones (Fact Decay)

Idea: revisar una página buena que se quedó vieja y regalarle al editor una hoja fechada con lo
que ya no es cierto, cada punto con su fuente primaria.

1. Elegir páginas que importan: las del paso 8 o las que rankean para las consultas de dinero.
2. Sacar cada afirmación comprobable: cifras, precios, fechas, nombres, "el más reciente", "hoy".
3. Verificar cada una contra la **fuente primaria** (página de precios del fabricante, estudio
   original, comunicado, norma oficial). No contra otro blog.
4. Clasificar: vigente, cambió, superada, no se pudo verificar. Lo no verificado se marca así y
   no se envía como corrección.
5. Armar la hoja: afirmación, estado, fuente con URL, oración de reemplazo escrita en la voz de
   la página para que se pueda pegar.
6. **Primer correo sin pedir enlace.** La hoja es todo el mensaje. El enlace llega cuando la
   oración corregida necesita una fuente y el cliente es esa fuente, o en la segunda vuelta.

Entregable: una hoja por página, fechada, cada fila con fuente. Esqueleto del correo: qué página,
cuántos datos cambiaron, dos ejemplos concretos, la hoja adjunta, ninguna petición.

Costo real: la verificación es trabajo humano. Rápido aquí no vale nada; equivocado cuesta caro.

## 2. Lápida (Tombstone)

Idea: listas de "los mejores" y comparativas que siguen recomendando un producto o despacho que
cerró, se fusionó o dejó el segmento. La URL responde bien, así que ninguna herramienta de enlaces
rotos lo marca.

1. Lista de bajas en la categoría del cliente: avisos de cierre, adquisiciones, productos
   descontinuados, precios que pasaron a "contacta a ventas", cambios de segmento.
2. **Recibo de cada baja:** URL del aviso, fecha, captura. Sin recibo no hay correo.
3. Encontrar quién la sigue listando: el censo del paso 8 primero (una baja en una página que los
   asistentes citan vale más que cualquier otra); luego búsqueda del nombre con patrones de lista.
4. Por página: qué entrada quedó vieja, el recibo, y el texto de reemplazo para ese lugar escrito
   en la voz de la página. Si la alternativa más cercana no es el cliente, se dice cuál es.

Entregable por página: URL, entrada vieja, recibo, texto de reemplazo y contacto verificado.
Esqueleto del correo: qué entrada, desde cuándo y con qué prueba, y el texto listo para pegar.

## 3. Visual faltante (Missing Visual)

Idea: una página que ya posiciona describe en prosa un proceso, una comparación o una línea de
tiempo y no tiene ningún diagrama. Se le hace ese diagrama **con su propio texto**.

1. Candidatas: páginas que rankean o que el paso 8 encontró, con cero o una imagen en el cuerpo.
2. Comprobar que la prosa tiene forma: pasos numerados, opciones comparables, fechas, jerarquía o
   un set de cifras. Si no la tiene, se descarta; forzar un diagrama sobre prosa sin forma se nota.
3. Construir desde código (SVG o HTML a PNG), no con un generador de imágenes, que deforma el
   texto. Si hay sistema de diseño del cliente, se usa con discreción: el diagrama es del editor.
4. **Ni una cifra que no esté en su texto.** El argumento entero es que el visual es su artículo.
5. Dos versiones: una con crédito pequeño al cliente y una limpia. Se ofrece la limpia sin
   condiciones.

Entregable por página: el visual en dos versiones y el borrador. Esqueleto del correo: qué sección
describe qué, el diagrama hecho con sus palabras, adjunto, el crédito es opcional.

## Qué no se hace

| No | Por qué |
|---|---|
| Intercambio de enlaces o redes de "enlace por enlace" | Spam de enlaces según la política de Google [O] |
| Pagar por entrar a listas de "los mejores" | Se detecta, no dura, contamina la entidad; en salud es violación publicitaria |
| Campañas pagadas en Reddit, Quora o YouTube que se presentan como opinión de usuarios | Astroturfing; mismo problema que pagar por aparecer |
| Registrarse en directorios gubernamentales o institucionales solo para sacar un enlace | No es una superficie que el comprador consulte; el enlace no es el objetivo |
| Plantilla enviada a cientos de sitios | El método depende de que se note hecho a mano |
| Afirmar algo sobre la página ajena sin fuente primaria | Una corrección equivocada termina la relación |

## Y en el sitio propio

El activo que más se cita es el que tiene datos con fuente: una **página de datos** propia con el
filtro de `geo-aeo.md` (fuente nombrada, año, cifra exacta, URL abierta, cita fiel, enlace vivo y
fuentes enlazadas). Es lo que hace que el editor tenga a quién enlazar cuando corrige su página.
