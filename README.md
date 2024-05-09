# Vendor Management System with Performance Metrics

A Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics. Please read the below documentation to understand how to interact with the various API endpoints.

## Prerequisites 

- IDE
- MySQL
- Postman (requiered for token-based authentication)

## Getting Started

### Installing libraries
    
    pip install django
    pip install djangorestframework
    pip install mysqlclient

### Database Connection

If you're using MySQL, make sure to configure the database settings (`settings.py`). 

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',       # Database engine
            'NAME': 'vendor_system',                    # Database name
            'USER': 'mydatabaseuser',                   # Database user (usually root)
            'PASSWORD': 'mypassword',                   # Database password
            'HOST': 'localhost',                        # Database host
            'PORT': '3306',                             # Database port
        }
    }

You can interact with the database using the MySQL CMD Line Client or use the command below to connect to the MySQL server using your username, with the server prompting you to enter the password for the user.
    
    mysql -u your_user_name -p 
    create database vendor_system;

### Setting up Postman

Postman is a tool for testing and interacting with APIs. To set up Postman for interacting with the APIs, create a new collection named "VendorManagementSystem" and add requests within it. Right-click on the collection to add a request, then choose the HTTP request method `(GET, POST, PUT, DELETE)` and paste the corresponding URL for the desired API endpoint. Input data can be entered by selecting `Body` tab, then choosing `raw and JSON` format, and pasting the data accordingly. Ensure to follow the provided examples for input data structure.

### Token-based Authentication

The API endpoints have been secured with token-based authentication. Create credentials using `python manage.py createsuperuser`. To obtain a token for a session, paste the `api/token/` endpoint and choose the HTTP request method `POST` on Postman. Credentials can be entered by:

```json
{
    "username": "username",
    "password": "password"
}
```
A token will be displayed in the output. Please save this token for futher use. To use the endpoints, select the `Header` tab, then enter `Authorization` under Key and `Token token_number` under Value. You now have access to the endpoint. This must be done for all endpoints. If not:

    {
        "detail": "Authentication credentials were not provided."
    }

## API Endpoints: Vendor Profile Management

### List All Vendors and Create New Vendor `GET | POST`
        
URL: `api/vendors/`

Description: Lists all the vendors available in the database and allows creation of new vendors

Input data:

```json
{
    "name": "John Doe",
    "contact_details": "johndoe@abcinc.com, +123456789",
    "address": "USA",
    "vendor_code": "ven1"
}
```

#### Test Scenarios

Scenario: Retrieve All Vendor data (HTTP 200 OK)

```json
{
    "id": 1,
    "name": "John Doe",
    "contact_details": "johndoe@abcinc.com, +123456789",
    "address": "USA",
    "vendor_code": "ven1"
}
{
    "id": 2,
    "name": "Elizabeth",
    "contact_details": "ellie@gmail.com",
    "address": "Las Vegas",
    "vendor_code": "ven2"
}
```

### Retrieve, Update, or Delete Specific Vendor `GET | PUT | DELETE`

URL: `api/vendors/{vendor_id}`

Description: Retrieves a specific vendor's details, with option to update or delete their information as needed. Updates can be partial or all details.

Updating/ Modifying data:

```json
{
    "contact_details": "johndoe@gmail.com, +9876543210",
    "address": "California, USA",
}
```        

#### Test Scenarios

Scenario: Delete a Vendor

```json
{
    "message": "Vendor deleted successfully"
}
```

### Retrieve Vendor Performance Metrics `GET`

URL: `api/vendors/{vendor_id}/performance`

Description: Retrieves a specific vendor's performance metrics, namely on-time delivery rate, average quality rating, average response time and fulfillment_rate.

Initial Response:

```json    
{
    "on_time_delivery_rate (%)": 0,
    "quality_rating_average (out of 5)": 0,
    "average_response_time (in hours)": 0,
    "fulfilment_rate (%)": 0
}
```

#### Test Scenarios

Scenario: Retrieve Performance Metrics Data (HTTP 200 OK)

```json
{
    "vendor": 1,
    "date": "2024-05-09T04:39:24.659179Z",
    "on_time_delivery_rate (%)": 0.0,
    "quality_rating_average (out of 5)": 0.0,
    "average_response_time (in hours)": 0.0,
    "fulfilment_rate (%)": 0.0
}
```

## API Endpoints: Purchase Order Tracking

### List All Purchase Orders and Create New Purchase Order `GET | POST`

URL: `api/purchase_orders/`

Description: Lists all the purchase orders available in the database and allows creation of new purchase orders. Delivery date refers to the expected delivery date and the actual delivery date is assumed to be a week from the order date.

Input data:

```json
{
    "po_number": "PO1",
    "vendor": 1,
    "order_date": "2024-05-01T10:00:00",
    "delivery_date": "2024-05-13T10:00:00",
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
    "issue_date": "2024-05-01T10:00:00"
}
```

#### Test Scenarios

Scenario: If vendor ID is not specified while creation of purchase order

```json
{
    "message": "Vendor ID must be provided. ('vendor' : id)"
}
```

Scenario: If number of items specified and quanity value do not match
```json
{
    "non_field_errors": [
        "The number of items and quantity do not match"
    ]
}
```

Scenario: If expected delivery date is a date before the order date
```json
{
    "non_field_errors": [
        "The delivery date is before the order date"
    ]
}
```

### Retrieve, Update, or Delete Specific Purchase Order `GET | PUT | DELETE`

URL: `api/purchase_orders/{po_id}`

Description: Retrieves a specific purchase order's details, with option to update or delete their information as needed. Updates can be partial or all details.

Updating/Modifying data:

```json
{
     "items": [
    {
      "name": "Purse",      
      "unit_price": 60.00
    },
    {
      "name": "Tote Bag",
      "unit_price": 80.00
    }
    ],
}
```

#### Test Scenarios

Scenario: Delete an Order

```json
{
    "message": "Order deleted successfully"
}
```

### Vendor Acknowledge Purchase Order `POST`

URL: `api/purchase_orders/{po_id}/acknowledge`

Description: Vendor can acknowledges a specific purchase order.

Input data:

```json
{
      "acknowledgment_date": "2024-05-01T11:00:00"
}
```

If acknowledgment field is entered, the status of the purchase order automatically updates to `completed`. 

#### Test Scenarios

Scenario: If acknowledgment date is a date that is before the issue date

```json
{
    "non_field_errors": [
        "The acknowledgment date is before the issue date"
    ]
}
```

### Rate Purchase Order Quality `POST`

URL: `api/purchase_orders/{po_id}/quality_rate`

Input data:

```json
{
    "quality_rate": 3.5
}
```

#### Test Scenarios

Scenario: If quality rating isn't within the range of [1-5]

```json
{
    "non_field_errors": [
        "Quality rating must be between 1 and 5."
    ]
}
```

## Error Responses

The following error response is returned when a resource number `(vendor_code, po_number)` already exists in the database:

```json
{
    "po_number": [
        "purchase order with this PO Number already exists."
    ]
}
```
```json
{
    "vendor_code": [
        "vendor with this Vendor Code already exists."
    ]
}
```

The following error response is returned when a resource `(Vendor, Purchase order)` is not found in the database with the specified ID:

```json
{
    "message": "No Vendor found with the specified ID"
}
```
```json
{
    "message": "No Purchase Order found with the specified ID"
}
```

## Historical Model

The HistoricalPerformance model stores historical data on vendor performance, allowing for trend analysis. It can be viewed using `select * from performance`. This model stores records of vendors evertime there is a change in the metrics. 

### Database Queries (in case you want to restart)

    DELETE FROM orders;
    DELETE FROM performance;
    DELETE FROM vendor;
    
    ALTER TABLE vendor AUTO_INCREMENT = 1;
    ALTER TABLE orders AUTO_INCREMENT = 1;
    ALTER TABLE performance AUTO_INCREMENT = 1;

### Important Notes
```json
- THE ACTUAL DELIVERY DATE OF THE PRODUCTS IS ASSUMED TO BE A WEEK FROM THE ORDER DATE since it wasn't explicitly stated in the assingment
- Please ensure to read the documentation carefully before using any API endpoints.
- Feedback and contributions are welcome. Feel free to submit any issues if you encounter any problems. 
```
