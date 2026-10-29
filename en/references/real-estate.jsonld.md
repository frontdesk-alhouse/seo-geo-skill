# Real estate: JSON-LD (extends baseline)

Typical case: a developer or brokerage with listings in a CMS (fictional example: Inmobiliaria Cantera,
a Mexican brokerage). Use this **on top of** the baseline (Organization/WebSite/BreadcrumbList).
Ideal for binding to a listings CMS.

> Honest reality: real estate listing rich results in Google are **limited**. The value here is
> entity clarity + AI visibility, not a guaranteed visual result.

---

## 1. RealEstateAgent (home / agency page)

A subtype of `LocalBusiness`; it inherits address, hours, phone (see `local-seo.md`).

```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "{{business_name}}",
  "url": "https://{{domain}}/",
  "image": "https://{{domain}}/{{image_path}}",
  "telephone": "{{phone_e164}}",
  "priceRange": "{{$$-$$$}}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{street_address}}",
    "addressLocality": "{{city}}",
    "addressRegion": "{{state}}",
    "postalCode": "{{postal_code}}",
    "addressCountry": "MX"
  },
  "areaServed": "{{area_or_city}}"
}
```

## 2. RealEstateListing (per property: CMS-bound)

One per property page. In Webflow, a Collection template with bound fields.

```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateListing",
  "url": "https://{{domain}}/properties/{{ Slug }}",
  "name": "{{ Property Name }}",
  "datePosted": "{{ Date Posted }}",
  "image": "{{ Main Image }}",
  "description": "{{ Description }}",
  "offers": {
    "@type": "Offer",
    "price": "{{ Price }}",
    "priceCurrency": "MXN",
    "availability": "https://schema.org/InStock"
  },
  "about": {
    "@type": "Residence",
    "name": "{{ Property Name }}",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "{{ City }}",
      "addressRegion": "{{ State }}",
      "addressCountry": "MX"
    }
  }
}
```

## 3. Residence / House / Apartment (property details)

Use the most specific subtype: `House`, `Apartment`, `SingleFamilyResidence`.

```json
{
  "@context": "https://schema.org",
  "@type": "{{House|Apartment|SingleFamilyResidence}}",
  "name": "{{ Property Name }}",
  "numberOfRooms": "{{ Bedrooms }}",
  "numberOfBathroomsTotal": "{{ Bathrooms }}",
  "floorSize": {
    "@type": "QuantitativeValue",
    "value": "{{ Square Meters }}",
    "unitCode": "MTK"
  }
}
```

---

## Binding in the Webflow CMS: careful

Fields that **DO** bind: Plain text, Image, Video link, Link, Email, Phone, Number, Date/Time,
Switch, Color, Option, File.

Fields that do **NOT** bind: **Reference, Multi-reference, Multi-image**. If you need data from a
reference (e.g. the assigned agent), restructure it into a Plain text/Option field in the properties
collection.
