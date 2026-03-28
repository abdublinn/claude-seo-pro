# LocalBusiness Schema Subtypes by Industry

## How to Choose

Use the most specific subtype available. `LocalBusiness` is a fallback — always prefer a subtype.

## Common Subtypes

| Industry | Schema Type | Key Properties |
|----------|-------------|---------------|
| **Furniture store** | `FurnitureStore` | priceRange, paymentAccepted, openingHours |
| **Restaurant** | `Restaurant` | servesCuisine, menu, acceptsReservations |
| **Auto repair** | `AutoRepair` | — |
| **Beauty salon** | `BeautySalon` | — |
| **Dental** | `Dentist` | medicalSpecialty |
| **Law firm** | `LegalService` | — |
| **Real estate** | `RealEstateAgent` | — |
| **Gym/fitness** | `HealthClub` | — |
| **Hotel** | `Hotel` | starRating, checkinTime |
| **Store (general)** | `Store` | — |
| **Home improvement** | `HomeAndConstructionBusiness` | — |
| **Medical** | `MedicalBusiness` | medicalSpecialty |
| **Pet services** | `PetStore` or `AnimalShelter` | — |
| **Education** | `EducationalOrganization` | — |
| **Clothing** | `ClothingStore` | — |
| **Electronics** | `ElectronicsStore` | — |

## Required Properties (all subtypes)

```json
{
  "@context": "https://schema.org",
  "@type": "FurnitureStore",
  "name": "Store Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "image": "https://example.com/storefront.jpg",
  "telephone": "+7-XXX-XXX-XX-XX",
  "email": "info@example.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ул. Примерная, 1",
    "addressLocality": "Казань",
    "addressRegion": "Республика Татарстан",
    "postalCode": "420000",
    "addressCountry": "RU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 55.7887,
    "longitude": 49.1221
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "09:00",
      "closes": "18:00"
    }
  ],
  "priceRange": "₽₽",
  "paymentAccepted": "Cash, Credit Card, Bank Transfer",
  "sameAs": [
    "https://vk.com/storename",
    "https://t.me/storename",
    "https://yandex.ru/maps/org/storename/123456789/"
  ]
}
```

## Multi-Location Pattern

For businesses with multiple locations, use an `Organization` parent with `department` array pointing to individual `LocalBusiness` entries per location.
