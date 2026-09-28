-- 1. Create logical schemas to separate the load (Staging) from the business model (Retail)
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS retail;