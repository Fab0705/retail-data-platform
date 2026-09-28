# Data Warehouse Dictionary (Data Contract)

Este documento sirve como el contrato de datos técnico para el modelo Star Schema en PostgreSQL. Define la estructura física, llaves y reglas de negocio.

---

## 1. Fact Tables

### TABLE: FactSales
* **Purpose:** Stores retail transaction lines.
* **Grain:** One product line belonging to one transaction.
* **Primary Key:** `sales_key`.
* **Business Identifiers:** `transaction_id` + `product_id`.

| Column | Data Type | Nullable? | Description | Business Rule |
| :--- | :--- | :--- | :--- | :--- |
| `sales_key` | SERIAL | No | Llave primaria subrogada. | Autoincremental. |
| `date_key` | INT | No | DimDate's Foreign Key. | Formato YYYYMMDD. |
| `customer_key` | INT | No | DimCustomer's Foreign Key. | It must exist in DimCustomer. |
| `product_key` | INT | No | DimProduct's Foreign Key. | It must exist in DimProduct. |
| `store_key` | INT | No | DimStore's Foreign Key. | It must exist in DimStore. |
| `transaction_id` | VARCHAR(50) | No | Original transaction ID. | - |
| `quantity` | INT | No | Unidades compradas. | Must be > 0. |
| `unit_price` | NUMERIC(10,2) | No | Unit price at the time of purchase. | Must be >= 0. |
| `currency_code` | VARCHAR(3) | No | Sale currency. | Estándar ISO 4217 (ej. USD). |

---

### TABLE: FactEconomicIndicators
* **Purpose:** Stores annual macroeconomic observations.
* **Grain:** One country + indicator + year.
* **Primary Key:** `economic_indicator_key`.
* **Natural/Business Key:** `country_key` + `date_key` + `indicator_code`.

| Column | Data Type | Nullable? | Description | Business Rule |
| :--- | :--- | :--- | :--- | :--- |
| `economic_indicator_key` | SERIAL | No | Surrogate primary key. | Auto-incrementing. |
| `country_key` | INT | No | DimCountry's Foreign Key. | It must exist in DimCountry. |
| `date_key` | INT | No | DimDate's Foreign Key. | Formato YYYY (anual). |
| `indicator_code` | VARCHAR(50) | No | World Bank API Code. | Ej. 'NY.GDP.MKTP.CD'. |
| `indicator_name` | VARCHAR(255) | No | Descriptive name of the indicator. | Preserve original metadata. |
| `value` | NUMERIC | Yes | Value of the economic indicator. | It may be zero if the country did not report it that year.. |

---

## 2. Dimension Tables

### TABLE: DimCustomer
* **Purpose:** Stores descriptive attributes of retail customers.
* **Grain:** One record per unique customer.
* **Primary Key:** `customer_key`
* **Natural Key:** `customer_id`

| Column | Data Type | Nullable? | Description | Business Rule |
| :--- | :--- | :--- | :--- | :--- |
| `customer_key` | SERIAL | No | Surrogate primary key. | Auto-incrementing. |
| `customer_id` | VARCHAR(50) | No | Original ID from the source system. | Unique by customer. |
| `customer_name` | VARCHAR(100) | No | Full Name. | - |
| `gender` | VARCHAR(20) | Yes | Customer gender. | Standardized options (M, F, Other, N/A). |
| `country_code` | VARCHAR(3) | No | Country of residence. | ISO 3166-1 alpha-3. |
| `customer_segment` | VARCHAR(50) | No | Comercial Classification. | Premium, Standard, etc. |

### TABLE: DimProduct
* **Purpose:** Stores the retail product catalog.
* **Grain:** One record per unique product.
* **Primary Key:** `product_key`
* **Natural Key:** `product_id`

| Column | Data Type | Nullable? | Description | Business Rule |
| :--- | :--- | :--- | :--- | :--- |
| `product_key` | SERIAL | No | Surrogate primary key. | Auto-incrementing. |
| `product_id` | VARCHAR(50) | No | SKU/ID catalog. | Unique by product. |
| `product_name` | VARCHAR(150) | No | Product name. | - |
| `category` | VARCHAR(50) | No | Main category. | - |
| `brand` | VARCHAR(50) | Yes | Product brand. | - |