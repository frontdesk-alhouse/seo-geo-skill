# Local SEO: LocalBusiness + Google Business Profile + NAP

> Ported and adapted from concepts in `AgriciDaniel/claude-seo` (v2.2.4, MIT). For businesses
> with a physical presence or that serve an area (real estate agency, medical practice, kitchen
> showroom).

Local SEO lives in two layers that must **match exactly**: the site's `LocalBusiness` schema and
the Google Business Profile (GBP). NAP consistency is the foundation.

---

## NAP: Name, Address, Phone (consistency = everything)

The **same** name, address and phone, written **identically**, on: the site (schema + visible
text), GBP, and every directory. Differences ("Ave." vs "Avenue", phone with or without area
code) dilute the local signal.

- **Name**: the real business name, no keyword stuffing ("Example Realty", not "Example Realty
  Cheap Apartments Brooklyn NYC").
- **Address**: consistent format, with postal code.
- **Phone**: one local number, same format everywhere.

## LocalBusiness schema (choose the most specific subtype)

Instead of a generic `Organization` on the home page, use the subtype:
- Real estate agency → `RealEstateAgent`
- Medical → `MedicalClinic` / `Physician`
- Showroom/store → `Store` / `HomeGoodsStore`

```json
{
  "@context": "https://schema.org",
  "@type": "{{subtype}}",
  "name": "{{nap_name}}",
  "image": "https://{{domain}}/{{image}}",
  "telephone": "{{nap_phone}}",
  "priceRange": "{{$$-$$$}}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{nap_street}}",
    "addressLocality": "{{city}}",
    "addressRegion": "{{state}}",
    "postalCode": "{{postal_code}}",
    "addressCountry": "MX"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "{{lat}}",
    "longitude": "{{lng}}"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "09:00",
      "closes": "18:00"
    }
  ],
  "areaServed": "{{city_or_area}}"
}
```

`addressCountry` takes the ISO country code of the business (`MX`, `US`, ...).

## Google Business Profile: checklist

- [ ] Profile claimed and verified.
- [ ] Correct primary category + relevant secondary ones.
- [ ] NAP identical to the site's.
- [ ] Real, current hours (including holidays).
- [ ] Real photos (no stock).
- [ ] Reviews: actively ask real customers; reply to all of them (good and bad).
- [ ] Products/services listed.

## Directories

- **Mexico:** NAP consistency on Google Business Profile, Facebook, industry directories. For
  physicians, **Doctoralia** and other vertical directories: see `entity-sameas.md`.
- **US:** the same on Google Business Profile, Facebook, Yelp, BBB and industry directories. For
  physicians, Healthgrades and Zocdoc: see `entity-sameas.md`.
