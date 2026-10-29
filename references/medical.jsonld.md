# Médico / cirujano: JSON-LD (extiende baseline)

Caso tipo: un cirujano con subespecialidad angosta (ejemplo ficticio: Dra. Elena Ruiz, cirugía de
columna, Monterrey). Usa esto **encima** del baseline. Correcciones clave (validadas contra schema.org v30):

> **Zona YMYL (Your Money Your Life).** Google exige E-E-A-T más que en ningún otro vertical:
> autoría con credenciales reales, precisión factual, citas. El schema ayuda a la claridad de
> entidad, pero el peso del ranking está en la autoridad demostrable del especialista.

## Reglas de modelado (leer antes de escribir)

1. **Separar la PERSONA de la ENTIDAD clínica.** `Physician` en schema.org **no hereda de
   `Person`**, es una organización médica. Por eso `alumniOf`, `worksFor`, `jobTitle`,
   `memberOf` (biográficas) **NO** van en `Physician`: van en un nodo **`Person`**. Modela dos
   nodos: `Person` (el doctor, con credenciales) + la entidad clínica.
2. **Entidad clínica según la realidad:**
   - Consultorio propio → `MedicalClinic` (subtipo de `LocalBusiness`).
   - Solo pasa consulta en hospital ajeno, sin consultorio propio → `IndividualPhysician` con
     `practicesAt` → el hospital. No fabriques una clínica que no existe.
3. **Varias sedes reales** = varios nodos de ubicación (`MedicalClinic`) con `parentOrganization`
   → la práctica. Esto es legítimo **solo si son ubicaciones físicas reales**, no inventes una
   sede por ciudad (eso es doorway page, penalizado por Google).
4. **`@id` canónico** reusado en toda página (ver `baseline.jsonld.md`): `#practice`, `#dr`,
   `#website`.

---

## 1. Person: el médico (credenciales, E-E-A-T)

Las propiedades biográficas viven AQUÍ, no en `Physician`/`MedicalClinic`.

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://{{domain}}/#dr",
  "name": "Dr. {{nombre_completo}}",
  "url": "https://{{domain}}/{{sobre_slug}}",
  "image": "https://{{domain}}/{{foto_path}}",
  "jobTitle": "{{cargo, ej. Jefe de Neurocirugía, Hospital X}}",
  "alumniOf": [
    { "@type": "CollegeOrUniversity", "name": "{{universidad_1}}" },
    { "@type": "CollegeOrUniversity", "name": "{{universidad_2}}" }
  ],
  "memberOf": { "@type": "Organization", "name": "{{colegio_o_asociacion}}" },
  "worksFor": { "@id": "https://{{domain}}/#practice" }
}
```
> `hasCredential` (`EducationalOccupationalCredential`) es más preciso que `memberOf` para una
> distinción tipo "SNI I" o una certificación de consejo, verifica caso por caso qué es realmente.

## 2. MedicalClinic: la práctica (consultorio propio)

`medicalSpecialty` usa **valores reales del enum** (no existen "Neurosurgery" ni "Endocrinology";
usa `Neurologic`, `Surgical`, `Oncologic`, `Endocrine`). Enlaza al médico como `member`.

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalClinic",
  "@id": "https://{{domain}}/#practice",
  "name": "{{clinic_name}}",
  "url": "https://{{domain}}/",
  "telephone": "{{+52...}}",
  "medicalSpecialty": [
    "https://schema.org/Neurologic",
    "https://schema.org/Surgical",
    "https://schema.org/Oncologic"
  ],
  "member": { "@id": "https://{{domain}}/#dr" },
  "availableService": { "@id": "https://{{domain}}/#procedimiento" },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{calle_numero}}",
    "addressLocality": "{{ciudad}}",
    "addressRegion": "{{estado}}",
    "postalCode": "{{cp}}",
    "addressCountry": "MX"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": "{{lat_5+decimales}}", "longitude": "{{lng_5+decimales}}" },
  "areaServed": [
    { "@type": "Country", "name": "México" },
    { "@type": "City", "name": "{{ciudad}}" }
  ],
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00" }
  ]
}
```
> **Varias sedes:** repite un nodo `MedicalClinic` por sede real (cada uno con su `address`+`geo`+
> `telephone`) y añádele `"parentOrganization": { "@id": "https://{{domain}}/#practice" }`.
> `geo` con **mínimo 5 decimales**, del pin real (Google Maps → click derecho → "¿Qué hay aquí?").

## 3. MedicalProcedure: por tratamiento

`SurgicalProcedure` es un **@type**, no un valor de `procedureType` (ese enum es
`MedicalProcedureType`). El médico/clínica enlaza el procedimiento con `availableService`, **no**
con `provider` (que no es dominio de `MedicalProcedure`).

```json
{
  "@context": "https://schema.org",
  "@type": "SurgicalProcedure",
  "@id": "https://{{domain}}/#procedimiento",
  "name": "{{nombre_procedimiento}}",
  "description": "{{descripcion_visible_en_pagina}}",
  "howPerformed": "{{resumen_del_procedimiento}}",
  "bodyLocation": "{{estructura_anatomica_real}}"
}
```

## 4. MedicalWebPage / condición: landings

Clasifica **cada** landing por lo que realmente es (no fuerces `MedicalCondition` a todo):
- Enfermedad/trastorno/síndrome → `MedicalCondition` (ej. prolactinoma, acromegalia, Cushing).
- Síntoma/signo → `MedicalSignOrSymptom` (ej. cefalea, "se me cierra la vista").
- `associatedAnatomy` **solo** cuando esa anatomía es de verdad el tema de la página.

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "@id": "https://{{domain}}/sintomas/{{slug}}/#webpage",
  "name": "{{titulo}}",
  "url": "https://{{domain}}/sintomas/{{slug}}",
  "inLanguage": "es-MX",
  "isPartOf": { "@id": "https://{{domain}}/#website" },
  "about": {
    "@type": "{{MedicalCondition|MedicalSignOrSymptom}}",
    "name": "{{nombre_clinico}}"
  },
  "author": { "@id": "https://{{domain}}/#dr" },
  "lastReviewed": "{{YYYY-MM-DD}}",
  "reviewedBy": { "@id": "https://{{domain}}/#dr" }
}
```
> `reviewedBy` **solo si hubo una revisión real**. Si el autor y el revisor son la misma persona y
> no existió un proceso de revisión separado, usa solo `author` + `lastReviewed` (no afirmes una
> revisión que no ocurrió).

## 5. ReserveAction: agendar (CONDICIONAL)

Añádelo **solo si existe una agenda online funcional** (no solo un WhatsApp/teléfono). No garantiza
un botón "Book" en IA (eso requiere Maps Booking API), es una señal, no una promesa.

```json
{
  "@type": "ReserveAction",
  "name": "Agendar consulta",
  "target": "https://{{url_de_agenda_online}}",
  "result": { "@type": "Reservation", "name": "Consulta con Dr. {{nombre}}" }
}
```

---

## Reglas específicas de salud

- **NO `Review`/`AggregateRating` copiados de Doctoralia/Google.** Google **prohíbe** agregar
  ratings de terceros y no muestra estrellas "self-serving" en `LocalBusiness`/`Organization`.
  Solo con reseñas **propias, reales y visibles en la página**.
- **`medicalSpecialty`** usa URLs del enum real (`https://schema.org/Neurologic`, etc.). No inventes
  valores.
- Cada claim médico respaldado: autor, fecha, fuente. Eso pesa más que el markup.
