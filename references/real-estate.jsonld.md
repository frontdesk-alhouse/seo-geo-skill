# Inmobiliaria: JSON-LD (extiende baseline)

Caso tipo: una desarrolladora o inmobiliaria con listados en CMS (ejemplo ficticio: Inmobiliaria Cantera). Usa esto **encima** del baseline (Organization/WebSite/
BreadcrumbList). Ideal para bindear a CMS de listados.

> Realidad honesta: los rich results de listados inmobiliarios en Google son **limitados**. El
> valor aquí es claridad de entidad + visibilidad en AI, no un resultado visual garantizado.

---

## 1. RealEstateAgent (home / página de la agencia)

Subtipo de `LocalBusiness`, hereda dirección, horario, teléfono (ver `local-seo.md`).

```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "{{business_name}}",
  "url": "https://{{domain}}/",
  "image": "https://{{domain}}/{{image_path}}",
  "telephone": "{{+52...}}",
  "priceRange": "{{$$-$$$}}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{calle_numero}}",
    "addressLocality": "{{ciudad}}",
    "addressRegion": "{{estado}}",
    "postalCode": "{{cp}}",
    "addressCountry": "MX"
  },
  "areaServed": "{{zona_o_ciudad}}"
}
```

## 2. RealEstateListing (por propiedad: CMS-bound)

Una por página de propiedad. En Webflow, template de Collection con campos bindeados.

```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateListing",
  "url": "https://{{domain}}/propiedades/{{ Slug }}",
  "name": "{{ Nombre Propiedad }}",
  "datePosted": "{{ Fecha Publicacion }}",
  "image": "{{ Imagen Principal }}",
  "description": "{{ Descripcion }}",
  "offers": {
    "@type": "Offer",
    "price": "{{ Precio }}",
    "priceCurrency": "MXN",
    "availability": "https://schema.org/InStock"
  },
  "about": {
    "@type": "Residence",
    "name": "{{ Nombre Propiedad }}",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "{{ Ciudad }}",
      "addressRegion": "{{ Estado }}",
      "addressCountry": "MX"
    }
  }
}
```

## 3. Residence / House / Apartment (detalle del inmueble)

Usa el subtipo más específico: `House`, `Apartment`, `SingleFamilyResidence`.

```json
{
  "@context": "https://schema.org",
  "@type": "{{House|Apartment|SingleFamilyResidence}}",
  "name": "{{ Nombre Propiedad }}",
  "numberOfRooms": "{{ Recamaras }}",
  "numberOfBathroomsTotal": "{{ Banos }}",
  "floorSize": {
    "@type": "QuantitativeValue",
    "value": "{{ M2 }}",
    "unitCode": "MTK"
  }
}
```

---

## Binding en Webflow CMS: cuidado

Campos que **SÍ** bindean: Plain text, Image, Video link, Link, Email, Phone, Number, Date/Time,
Switch, Color, Option, File.

Campos que **NO** bindean: **Reference, Multi-reference, Multi-image**. Si necesitas datos de una
referencia (p. ej. el agente asignado), reestructura a un campo Plain text/Option en la colección
de propiedades.
