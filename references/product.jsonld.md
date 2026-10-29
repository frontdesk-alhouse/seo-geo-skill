# Catálogo de producto: JSON-LD (extiende baseline)

Caso tipo: un catálogo industrial grande (más de mil variantes, colecciones Sistemas +
Variantes en Webflow; ejemplo ficticio: Aceros del Bajío). Usa esto **encima** del baseline.

> **Aquí es donde MÁS rich results visuales hay** (precio, disponibilidad, estrellas). Pero
> `Product` genérico da poca ventaja: puebla precio, disponibilidad, rating y specs concretas.

---

## 1. Product + Offer (por producto/variante: CMS-bound)

Una por página de producto. En Webflow, template de Collection con campos bindeados.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{ Nombre Producto }}",
  "image": "{{ Imagen Principal }}",
  "description": "{{ Descripcion }}",
  "sku": "{{ SKU }}",
  "brand": {
    "@type": "Brand",
    "name": "{{ Marca }}"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://{{domain}}/sistemas/{{ Slug }}",
    "priceCurrency": "MXN",
    "price": "{{ Precio }}",
    "availability": "https://schema.org/{{InStock|OutOfStock|PreOrder}}",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
```

> `price` sin símbolo de moneda ni separador de miles ("14500", no "$14,500"). `priceCurrency`
> aparte. Si el catálogo no muestra precio público, **omite `offers.price`**, no inventes uno.

## 2. AggregateRating + Review (solo si existen)

Agrega esto dentro de `Product` **únicamente** si hay reseñas reales visibles en la página.

```json
{
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{ Rating Promedio }}",
    "reviewCount": "{{ Total Resenas }}"
  },
  "review": [
    {
      "@type": "Review",
      "author": { "@type": "Person", "name": "{{ Autor }}" },
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "{{ Rating }}",
        "bestRating": "5"
      },
      "reviewBody": "{{ Texto Resena }}"
    }
  ]
}
```

## 3. Sistema como colección: ItemList (página de listado)

Para la página de un Sistema que agrupa variantes, un `ItemList` ayuda a la comprensión.

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "{{ Nombre Sistema }}",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "url": "https://{{domain}}/sistemas/{{ Slug Variante }}"
    }
  ]
}
```

---

## Reglas específicas de producto

- **Availability y price deben coincidir con lo visible.** Marcar "InStock" en algo agotado o un
  precio distinto al mostrado es violación de política y puede quitar elegibilidad de rich result.
- Alimenta también Merchant Center / Shopping si el cliente vende online (el mismo `Offer` sirve).
- Campos Webflow que **NO** bindean: Reference, Multi-reference, Multi-image. Un catálogo que
  ya usa nomenclatura de hoja de cálculo mapea SKU/Marca/Precio a campos Plain text/Number.
