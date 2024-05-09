# INPUT DATA STRUCTURES

## VENDORS

```json
{
    "name": "Elizabeth",
    "contact_details": "ellie@gmail.com",
    "address": "Las Vegas",
    "vendor_code": "ven1"
}
```
**Example for repetive vendor code**


```json
{
    "name": "Jane Smith",
    "contact_details": "janesmith@xyzcorp.com, +987654321",
    "address": "Paris, Rome",
    "vendor_code": "ven1"
}
```


## PURCHASE ORDERS

**Example for on time delivery**

```json
{
  "po_number": "PO1",
  "vendor": 1,
  "order_date": "2024-05-01T10:00:00",
  "delivery_date": "2024-05-5T10:00:00",
  "items": [
    {
      "name": "Product A",      
      "unit_price": 25.50
    },
    {
      "name": "Product B",
      "unit_price": 30.00
    }
  ],
  "quantity": 2,
  "status": "pending",
  "issue_date": "2024-05-01T10:00:00",
}
```

**Example for late delivery**

```json
{
  "po_number": "PO2",
  "vendor": 1,
  "order_date": "2024-05-01T10:00:00",
  "delivery_date": "2024-05-13T10:00:00",
  "items": [
    {
      "name": "Item A",      
      "unit_price": 50
    },
    {
      "name": "Item B",
      "unit_price": 40.00
    }
  ],
  "quantity": 2,
  "status": "pending",
  "issue_date": "2024-05-01T10:00:00",
}
```

**Example for mistmatched items and quantity value**

```json
{
  "po_number": "PO3",
  "vendor": 1,
  "order_date": "2024-05-01T10:00:00",
  "delivery_date": "2024-05-13T10:00:00",
  "items": [
    {
      "name": "A",      
      "unit_price": 25.50
    },
    {
      "name": "B",
      "unit_price": 30.00
    },
    {
      "name": "C",
      "unit_price": 30.00
    }
  ],
  "quantity": 1,
  "status": "pending",
  "issue_date": "2024-05-15T10:00:00",
}
```

## ACKNOWLEDGE 

```json
{
  "acknowledgment_date": "2024-05-03T11:00:00Z"
}
```

## QUALITY RATE

**Example for in range**

```json
{
    "quality_rate": 5
}
```

**Example for out range**

```json
{
    "quality_rate": 8
}
```
