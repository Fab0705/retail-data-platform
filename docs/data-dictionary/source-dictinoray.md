# SOURCE DATA DICTIONARY

This document defines the structure of the synthetically generated raw data (Retail) and the data extracted from the API (Economic).

## DOMAIN: RETAIL

### ENTITY: Customers
* **customer_id**: Unique customer identifier.
* **customer_name**: Customer full name.
* **gender**: Customer gender.
* **birth_date**: Birthdate.
* **country_code**: Country of residence code.
* **customer_segment**: Customer segment.
* **registration_date**: Date the customer registered.

### ENTITY: Products
* **product_id**: Unique product identifier.
* **product_name**: Product name.
* **category**: Main category.
* **subcategory**: Sub-category.
* **brand**: Product brand.
* **unit_cost**: Production/acquisition cost per unit.
* **unit_price**: Retail price per unit.

### ENTITY: Stores
* **store_id**: Unique store identifier.
* **store_name**: Store name.
* **country_code**: Country code of the location.
* **city**: City of the location.
* **store_type**: Store type or format.
* **opening_date**: Store opening date.

### ENTITY: Sales (Transacciones)
* **transaction_id**: Transaction/Order identifier.
* **transaction_date**: Transaction date and time.
* **customer_id**: Customer who made the purchase.
* **product_id**: Purchased product.
* **store_id**: Store where the purchase was made.
* **quantity**: Number of units purchased in this line item.
* **unit_price**: Unit price at the time of sale.
* **currency_code**: Transaction currency.

## DOMAIN: ECONOMIC (World Bank API)

### ENTITY: Macroeconomic Indicators
* **Country**: Country of observation.
* **Indicator**: Economic Indicator (ej. GDP, Inflation, Population).
* **Year**: Year of observation.