# DATA WAREHOUSE DICTIONARY

This document defines the analytical model (Star Schema) that will be hosted in PostgreSQL for consumption by Power BI.

## DIMENSIONAL TABLES (Dimensions)

**DimCustomer**
It contains the descriptive attributes of the customers.
* Columns: `customer_id`, `customer_name`, `gender`, `birth_date`, `country_code`, `customer_segment`, `registration_date`.

**DimProduct**
It contains the products catalog.
* Columns: `product_id`, `product_name`, `category`, `subcategory`, `brand`, `unit_cost`, `unit_price`.

**DimStore**
It contains information about the physical branches.
* Columns: `store_id`, `store_name`, `country_code`, `city`, `store_type`, `opening_date`.

## FACT TABLES (Facts)

**FactSales**
Fact table that records commercial sales.
* **Granularity:** One row for each transaction line. It is not one row per order.
* **Columns:** `transaction_id`, `transaction_date`, `customer_id`, `product_id`, `store_id`, `quantity`, `unit_price`, `currency_code`.
* **Métricas calculadas esperadas:** 
  * Total orders (`Orders`) = `DISTINCTCOUNT(transaction_id)`.
  * Revenue (`Revenue`) = `SUM(quantity * unit_price)`.

**FactEconomicIndicators**
Fact table recording the macroeconomic context from the World Bank.
* **Granularity:** An observation for a country, an indicator, and a year (ej. `PER | GDP | 2024`).
* **Columns:** `Country`, `Indicator`, `Year`.