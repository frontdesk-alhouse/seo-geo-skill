# Physician / surgeon: JSON-LD (extends baseline)

Typical case: a surgeon with a narrow subspecialty (fictional example: Dr. Elena Ruiz, spine surgery,
Monterrey, Mexico). Use this **on top of** the baseline. Key corrections (validated against schema.org v30):

> **YMYL zone (Your Money Your Life).** Google demands E-E-A-T here more than in any other vertical:
> authorship with real credentials, factual accuracy, citations. Schema helps entity clarity, but
> the ranking weight sits in the specialist's demonstrable authority.

## Modeling rules (read before writing)

1. **Separate the PERSON from the clinical ENTITY.** In schema.org, `Physician` **does not inherit
   from `Person`**: it is a medical organization. That is why `alumniOf`, `worksFor`, `jobTitle`,
   `memberOf` (biographical properties) do **NOT** go on `Physician`: they go on a **`Person`** node.
   Model two nodes: `Person` (the doctor, with credentials) + the clinical entity.
2. **Clinical entity according to reality:**
   - Own practice → `MedicalClinic` (a subtype of `LocalBusiness`).
   - Only sees patients at someone else's hospital, with no own practice → `IndividualPhysician` with
     `practicesAt` → the hospital. Do not fabricate a clinic that does not exist.
3. **Several real locations** = several location nodes (`MedicalClinic`) with `parentOrganization`
   → the practice. This is legitimate **only if they are real physical locations**. Do not invent a
   location per city (that is a doorway page, penalized by Google).
4. **Canonical `@id`** reused on every page (see `baseline.jsonld.md`): `#practice`, `#dr`,
   `#website`.

---

## 1. Person: the physician (credentials, E-E-A-T)

The biographical properties live HERE, not on `Physician`/`MedicalClinic`.

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://{{domain}}/#dr",
  "name": "Dr. {{full_name}}",
  "url": "https://{{domain}}/{{about_slug}}",
  "image": "https://{{domain}}/{{photo_path}}",
  "jobTitle": "{{job_title, e.g. Chief of Neurosurgery, Hospital X}}",
  "alumniOf": [
    { "@type": "CollegeOrUniversity", "name": "{{university_1}}" },
    { "@type": "CollegeOrUniversity", "name": "{{university_2}}" }
  ],
  "memberOf": { "@type": "Organization", "name": "{{medical_college_or_association}}" },
  "worksFor": { "@id": "https://{{domain}}/#practice" }
}
```
> `hasCredential` (`EducationalOccupationalCredential`) is more precise than `memberOf` for a
> distinction such as "SNI I" (Mexico's national researcher system) or a board certification.
> Check case by case what it really is.

## 2. MedicalClinic: the practice (own office)

`medicalSpecialty` uses **real enum values** ("Neurosurgery" and "Endocrinology" do not exist;
use `Neurologic`, `Surgical`, `Oncologic`, `Endocrine`). Link the physician as `member`.

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalClinic",
  "@id": "https://{{domain}}/#practice",
  "name": "{{clinic_name}}",
  "url": "https://{{domain}}/",
  "telephone": "{{phone_e164}}",
  "medicalSpecialty": [
    "https://schema.org/Neurologic",
    "https://schema.org/Surgical",
    "https://schema.org/Oncologic"
  ],
  "member": { "@id": "https://{{domain}}/#dr" },
  "availableService": { "@id": "https://{{domain}}/#procedure" },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{street_address}}",
    "addressLocality": "{{city}}",
    "addressRegion": "{{state}}",
    "postalCode": "{{postal_code}}",
    "addressCountry": "MX"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": "{{lat_5+_decimals}}", "longitude": "{{lng_5+_decimals}}" },
  "areaServed": [
    { "@type": "Country", "name": "Mexico" },
    { "@type": "City", "name": "{{city}}" }
  ],
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00" }
  ]
}
```
> **Several locations:** repeat one `MedicalClinic` node per real location (each with its own
> `address` + `geo` + `telephone`) and add `"parentOrganization": { "@id": "https://{{domain}}/#practice" }`.
> `geo` with **at least 5 decimals**, from the real pin (Google Maps → right-click → "What's here?").

## 3. MedicalProcedure: one per treatment

`SurgicalProcedure` is an **@type**, not a value of `procedureType` (that enum is
`MedicalProcedureType`). The physician/clinic links the procedure with `availableService`, **not**
with `provider` (which is not in the domain of `MedicalProcedure`).

```json
{
  "@context": "https://schema.org",
  "@type": "SurgicalProcedure",
  "@id": "https://{{domain}}/#procedure",
  "name": "{{procedure_name}}",
  "description": "{{description_visible_on_page}}",
  "howPerformed": "{{procedure_summary}}",
  "bodyLocation": "{{real_anatomical_structure}}"
}
```

## 4. MedicalWebPage / condition: landing pages

Classify **each** landing page by what it really is (do not force `MedicalCondition` onto everything):
- Disease/disorder/syndrome → `MedicalCondition` (e.g. prolactinoma, acromegaly, Cushing's).
- Symptom/sign → `MedicalSignOrSymptom` (e.g. headache, "my vision is closing in").
- `associatedAnatomy` **only** when that anatomy really is the topic of the page.

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "@id": "https://{{domain}}/symptoms/{{slug}}/#webpage",
  "name": "{{title}}",
  "url": "https://{{domain}}/symptoms/{{slug}}",
  "inLanguage": "en-US",
  "isPartOf": { "@id": "https://{{domain}}/#website" },
  "about": {
    "@type": "{{MedicalCondition|MedicalSignOrSymptom}}",
    "name": "{{clinical_name}}"
  },
  "author": { "@id": "https://{{domain}}/#dr" },
  "lastReviewed": "{{YYYY-MM-DD}}",
  "reviewedBy": { "@id": "https://{{domain}}/#dr" }
}
```
> `inLanguage` must match the language of the site (`en-US`, `es-MX`, ...).
>
> `reviewedBy` **only if a real review happened**. If the author and the reviewer are the same person
> and there was no separate review process, use only `author` + `lastReviewed` (do not claim a
> review that did not happen).

## 5. ReserveAction: booking (CONDITIONAL)

Add it **only if a working online booking system exists** (not just WhatsApp/phone). It does not
guarantee a "Book" button in AI (that requires the Maps Booking API); it is a signal, not a promise.

```json
{
  "@type": "ReserveAction",
  "name": "Book a consultation",
  "target": "https://{{online_booking_url}}",
  "result": { "@type": "Reservation", "name": "Consultation with Dr. {{name}}" }
}
```

---

## Health-specific rules

- **NO `Review`/`AggregateRating` copied from Doctoralia (Mexico), Healthgrades, Zocdoc or Google.**
  Google **prohibits** aggregating third-party ratings and does not show "self-serving" stars on
  `LocalBusiness`/`Organization`. Only with **your own, real reviews that are visible on the page**.
- **`medicalSpecialty`** uses URLs from the real enum (`https://schema.org/Neurologic`, etc.). Do not
  invent values.
- Every medical claim backed up: author, date, source. That weighs more than the markup.
