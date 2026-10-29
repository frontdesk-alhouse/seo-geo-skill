# Local SEO: LocalBusiness + Google Business Profile + NAP

> Portado y adaptado de conceptos de `AgriciDaniel/claude-seo` (v2.2.4, MIT). Para negocios con
> presencia física o que atienden una zona (inmobiliaria, consultorio médico, showroom de cocinas).

El SEO local vive en dos capas que deben **coincidir exactamente**: el schema `LocalBusiness` del
sitio y el perfil de Google Business Profile (GBP). La consistencia de NAP es el fundamento.

---

## NAP: Name, Address, Phone (consistencia = todo)

El **mismo** nombre, dirección y teléfono, escritos **idéntico**, en: el sitio (schema + texto
visible), GBP, y todos los directorios. Diferencias ("Av." vs "Avenida", teléfono con/sin lada)
diluyen la señal local.

- **Name**: el nombre comercial real, sin keyword stuffing ("Inmobiliaria Cantera", no "Inmobiliaria Cantera
  Departamentos Polanco CDMX Baratos").
- **Address**: formato consistente, con CP.
- **Phone**: un número local, mismo formato en todos lados.

## LocalBusiness schema (elige el subtipo más específico)

En vez de `Organization` genérico en la home, usa el subtipo:
- Inmobiliaria → `RealEstateAgent`
- Médico → `MedicalClinic` / `Physician`
- Showroom/tienda → `Store` / `HomeGoodsStore`

```json
{
  "@context": "https://schema.org",
  "@type": "{{subtipo}}",
  "name": "{{nap_name}}",
  "image": "https://{{domain}}/{{image}}",
  "telephone": "{{nap_phone}}",
  "priceRange": "{{$$-$$$}}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{nap_street}}",
    "addressLocality": "{{ciudad}}",
    "addressRegion": "{{estado}}",
    "postalCode": "{{cp}}",
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
  "areaServed": "{{ciudad_o_zona}}"
}
```

## Google Business Profile: checklist

- [ ] Perfil reclamado y verificado.
- [ ] Categoría primaria correcta + secundarias relevantes.
- [ ] NAP idéntico al del sitio.
- [ ] Horario real y actualizado (incluye festivos).
- [ ] Fotos reales (no stock).
- [ ] Reseñas: pedir activamente a clientes reales; responder todas (buenas y malas).
- [ ] Productos/servicios listados.

## Directorios (México)

Consistencia de NAP en: Google Business Profile, Facebook, directorios de industria. Para médicos,
**Doctoralia** y otros directorios verticales: ver `entidad-sameas.md`.
