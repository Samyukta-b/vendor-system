# INPUT DATA STRUCTURES

## VENDORS

{
    "name": "John Doe",
    "contact_details": "johndoe@abcinc.com, +123456789",
    "address": "123 Main Street, Anytown, USA",
    "vendor_code": "ven1"
}

{
    "name": "Jane Smith",
    "contact_details": "janesmith@xyzcorp.com, +987654321",
    "address": "456 Elm Street, Anycity, USA",
    "vendor_code": "ven2"
}

{
    "name": "Elizabeth",
    "contact_details": "ellie@gmail.com",
    "address": "Las Vegas",
    "vendor_code": "ven3"
}

## PURCHASE ORDERS

**Example for on time delivery**

{
  "po_number": "PO1",
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

**Example for late delivery**

{
  "po_number": "PO2",
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

**Example for mistmatched items and quantity value**

{
  "po_number": "PO2",
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

## ACKNOWLEDGE 

{
  "acknowledgment_date": "2024-05-03T11:00:00Z"
}

## QUALITY RATE

**Example for in range**

{
    "quality_rate": 5
}

**Example for out range**

{
    "quality_rate": 8
}
