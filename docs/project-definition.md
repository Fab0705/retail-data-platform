# BUSINESS PROBLEM
A retail company with a presence in multiple countries needs to understand its commercial performance and analyze how it relates to the macroeconomic context of each region. Currently, transactional data is isolated and lack a centralized, automated and reliable source that integrates them with external economic indicators to facilitate policy decision-making.
# OBJECTIVES
* Develop an end-to-end data platform that consolidates synthetic retail transactional data with real economic indicators from the World Bank API.
* Transform, validate and store this information in a relational analytical model (Star Schema) hosted in PostgreSQL.
* Expose modeled data via Power BI to enable business and economic analysis.
# BUSINESS QUESTIONS
**Commercials:**
* What is the total (revenue) income over time?
* Which products generate the most revenue?
* Which countries and stores have the best performance?
* What is the average value of the order (Average Order Value)?

**From Customers:**
* How many clients remain active?
* What is the customer generated income?
* Which customer segments generate the greatest value for the business?

**Economic context:**
* How does the economic environment vary (e.g. GDP, inflation, unemployment) by country over time?
* Do sales growth trends coincide with changes in external macroeconomic indicators?
# SCOPE
* Programmatic generation of synthetic transactional data (sales, customers, products, stores) using Python.
* Automated extraction of economic data using the World Bank API, implementing pagination.
* Development of an ETL pipeline in Python that includes cleaning, standardization and validation of business rules (Data Quality).
* Design and implementation of a dimensional model (Star Schema with Fact and Dim tables) in PostgreSQL.
* Development of logic for incremental loads (upserts) in the database.
* Creating a semantic model and interactive dashboard in Power BI.
# OUT OF SCOPE
* Real-time data processing and analytics (streaming). The system will operate through planned batch processing.
* Development of predictive models or machine learning algorithms.
* Construction of web applications or transactional user interfaces for manual data capture.
# EXPECTED OUTPUTS
* A professionally structured GitHub repository, including technical architecture documentation (diagrams) and decisions (DECISIONS.md).
* A PostgreSQL database deployed locally using Docker, populated with consistent data.
* Modular scripts in Python with unit testing and basic continuous integration.
* A Power BI report with separate executive views for business performance and economic context.