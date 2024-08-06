# Vulnerability Management Database

## Table of Contents
- [Introduction](#introduction)
- [ETL Design](#etl-design)
- [Data Model Explanation](#data-model-explanation)
- [Columns and Tables Explanation](#columns-and-tables-explanation)
- [Data Model Diagram](#data-model-diagram)
- [Connection to Postgres DB](#connection-to-postgres-db)
  - [Why PostgreSQL](#why-postgresql)
  - [Installation on Windows](#installation-on-windows)
  - [Installation on Mac](#installation-on-mac)
  - [Connecting to the Database](#connecting-to-the-database)
- [DDL Statements](#ddl-statements)
- [Loading Data into the DB](#loading-data-into-the-db)

## Introduction
This README file provides a comprehensive overview of the vulnerability management database, including ETL design, data model, and detailed explanation of tables and columns. This database is designed to store information about Common Vulnerabilities and Exposures (CVEs), their descriptions, related metrics, configurations, and other relevant data.

## ETL Design
The ETL (Extract, Transform, Load) process for this database involves the following steps:

### Extract
- **Source**: Data is extracted from the National Vulnerability Database (NVD) using three specific APIs:
  - **CVE Information**: Retrieved from the API at `https://services.nvd.nist.gov/rest/json/cves/2.0`. This API provides detailed information about vulnerabilities, including their descriptions, metrics, weaknesses, and configurations.
  - **CPE Information**: Retrieved from the API at `https://services.nvd.nist.gov/rest/json/cpes/2.0`. This API allows for the retrieval of detailed information on individual CPE records or collections of CPE records, which are essential for identifying vulnerable software and hardware configurations.
  - **Match Criteria Information**: Retrieved from the API at `https://services.nvd.nist.gov/rest/json/cpematch/2.0`. This API provides the complete list of valid CPE Match Strings, which are used to identify specific criteria for matching CPE records against vulnerabilities.

- **Data Types**: The extracted data includes various types of information, such as:
  - **CVE Information**: Includes the CVE ID, source identifier, publication date, last modified date, and vulnerability status. This data is stored in the `CVE` table.
  - **Descriptions**: Textual descriptions of CVEs in different languages, stored in the `Descriptions` table.
  - **Metrics**: CVSS metrics, including exploitability score, impact score, attack vector, base score, and severity, stored in the `CVSSMetric` table.
  - **Weaknesses**: Information about weaknesses related to each CVE, stored in the `Weaknesses` table.
  - **Configurations**: Configuration settings related to each CVE, stored in the `Configurations` table.
  - **Nodes and CPE Match Information**: Configuration nodes and criteria used for matching CPE records against vulnerabilities, stored in the `Nodes` and `CpeMatch` tables respectively.
  - **CPE Information**: Includes CPE names, their status (e.g., deprecated or not), and timestamps, stored in the `CPE` table.
  - **Match Criteria**: Information about match criteria for CPEs, including criteria strings and their statuses, stored in the `MatchString` table.


### Transform
- **Data Cleaning**: Removing duplicates, handling missing values, and normalizing data formats.
- **Data Enrichment**: Adding additional information like severity scores, exploitability scores, and impact scores.
- **Data Mapping**: Mapping the extracted data to the appropriate tables and columns in the database schema.

### Load
- **Database**: The cleaned and transformed data is loaded into the Postgres database using batch inserts or upserts to ensure data integrity and avoid duplicates.

## Data Model Explanation
The data model consists of several interconnected tables designed to store detailed information about CVEs and related data. The key entities in the data model include:

- **CVE**: Stores the main information about each CVE.
- **Descriptions**: Stores descriptions of each CVE in different languages.
- **CVSSMetric**: Stores CVSS metrics related to each CVE.
- **Source_type**: Stores information about the sources of CVSS metrics.
- **Weaknesses**: Stores weaknesses related to each CVE.
- **Weaknesses_Descriptions**: Stores descriptions of weaknesses in different languages.
- **Configurations**: Stores configuration settings related to each CVE.
- **Nodes**: Stores nodes related to configurations.
- **CpeMatch**: Stores CPE match information for nodes.
- **MatchString**: Stores match criteria for CPEs.
- **Matches**: Stores match details for CPE names.
- **CPE**: Stores information about CPE names.
- **Titles**: Stores titles and descriptions for CPE names.

## Columns and Tables Explanation

### CVE
- **cve_id**: Primary key, unique identifier for each CVE.
- **sourceIdentifier**: Identifier of the source reporting the CVE.
- **published**: Timestamp when the CVE was published.
- **lastModified**: Timestamp when the CVE was last modified.
- **vulnStatus**: Vulnerability status of the CVE.

### Descriptions
- **id**: Primary key, unique identifier for each description.
- **cve_id**: Foreign key, references `CVE(cve_id)`.
- **lang**: Language code for the description.
- **value**: Description text.

### CVSSMetric
- **id**: Primary key, unique identifier for each CVSS metric.
- **cve_id**: Foreign key, references `CVE(cve_id)`.
- **source_type_id**: Foreign key, references `Source_type(id)`.
- **version**: CVSS version.
- **exploitabilityScore**: Exploitability score.
- **impactScore**: Impact score.
- **attackVector**: Attack vector.
- **vectorString**: Vector string.
- **baseScore**: Base score.
- **baseSeverity**: Base severity.

### Source_type
- **id**: Primary key, unique identifier for each source type.
- **source**: Source of the CVSS metric.
- **type**: Type of the source.

### Weaknesses
- **id**: Primary key, unique identifier for each weakness.
- **cve_id**: Foreign key, references `CVE(cve_id)`.
- **source**: Source of the weakness.
- **type**: Type of the weakness.

### Weaknesses_Descriptions
- **id**: Primary key, unique identifier for each weakness description.
- **weakness_id**: Foreign key, references `Weaknesses(id)`.
- **lang**: Language code for the description.
- **value**: Description text.

### Configurations
- **id**: Primary key, unique identifier for each configuration.
- **cve_id**: Foreign key, references `CVE(cve_id)`.
- **operator**: Operator used in the configuration.

### Nodes
- **id**: Primary key, unique identifier for each node.
- **configuration_id**: Foreign key, references `Configurations(id)`.
- **operator**: Operator used in the node.
- **negate**: Boolean indicating if the node is negated.

### CpeMatch
- **id**: Primary key, unique identifier for each CPE match.
- **node_id**: Foreign key, references `Nodes(id)`.
- **vulnerable**: Boolean indicating if the CPE is vulnerable.
- **criteria**: Criteria used for matching.
- **matchCriteriaId**: Unique identifier for the match criteria.

### MatchString
- **matchCriteriaId**: Primary key, unique identifier for each match criteria.
- **criteria**: Match criteria string.
- **lastModified**: Timestamp when the match criteria was last modified.
- **cpeLastModified**: Timestamp when the related CPE was last modified.
- **created**: Timestamp when the match criteria was created.
- **status**: Status of the match criteria.

### Matches
- **id**: Primary key, unique identifier for each match.
- **matchCriteriaId**: Foreign key, references `MatchString(matchCriteriaId)`.
- **cpeName**: Name of the CPE.
- **cpeNameId**: Foreign key, references `CPE(cpeNameId)`.

### CPE
- **cpeNameId**: Primary key, unique identifier for each CPE name.
- **cpeName**: Name of the CPE.
- **deprecated**: Boolean indicating if the CPE is deprecated.
- **lastModified**: Timestamp when the CPE was last modified.
- **created**: Timestamp when the CPE was created.

### Titles
- **id**: Primary key, unique identifier for each title.
- **cpeNameId**: Foreign key, references `CPE(cpeNameId)`.
- **title**: Title of the CPE.
- **value**: Description text of the title.

## Data Model Diagram
![Data Model Diagram](https://github.com/bilalmasud07/DataCollectorAPI/blob/main/Vulnarabilities.png)

- **Vulnerabilities**: Central table storing main CVE information. It is related to:
  - **Descriptions**: Each CVE can have multiple descriptions in different languages. Linked via `cve_id`.
  - **CVSSMetric**: Each CVE can have multiple CVSS metrics. Linked via `cve_id`.
  - **Weaknesses**: Each CVE can have multiple weaknesses. Linked via `cve_id`.
  - **Configurations**: Each CVE can have multiple configurations. Linked via `cve_id`.

- **Descriptions**: Linked to `Vulnerabilities` through `cve_id`. Stores multilingual descriptions of CVEs.

- **CVSSMetric**: Linked to `Vulnerabilities` through `cve_id` and to `Source_type` through `source_type_id`. Stores CVSS metrics.

- **Source_type**: Linked to `CVSSMetric`. Stores information about the source of the CVSS metric.

- **Weaknesses**: Linked to `Vulnerabilities` through `cve_id`. Stores information about weaknesses.

- **Weaknesses_Descriptions**: Linked to `Weaknesses` through `weakness_id`. Stores descriptions of weaknesses in different languages.

- **Configurations**: Linked to `Vulnerabilities` through `cve_id`. Stores configuration settings.

- **Nodes**: Linked to `Configurations` through `configuration_id`. Stores nodes related to configurations.

- **CpeMatch**: Linked to `Nodes` through `node_id` and to `MatchString` through `matchCriteriaId`. Stores CPE match information.

- **MatchString**: Linked to `CpeMatch` and `Matches`. Stores match criteria for CPEs.

- **Matches**: Linked to `MatchString` through `matchCriteriaId` and to `CPE` through `cpeNameId`. Stores match details for CPE names.


## Connection to Postgres DB

### Why PostgreSQL
PostgreSQL is a powerful, open-source object-relational database system that offers several advantages for managing the vulnerability database:

- **Scalability**: PostgreSQL can handle large datasets, making it suitable for a database with millions of rows.
- **ACID Compliance**: Ensures data integrity and reliability by supporting transactions.
- **Advanced Features**: Includes support for advanced data types, indexing techniques, and performance optimization features.
- **Community Support**: PostgreSQL has a large and active community, providing extensive documentation and support.
- **Extensibility**: Allows the creation of custom functions, operators, and data types.

Given the need for normalization and the volume of data, PostgreSQL is an ideal choice for this project.

### Installation on Windows
1. Download the PostgreSQL installer from the [official website](https://www.postgresql.org/download/windows/).
2. Run the installer and follow the setup instructions.
3. During installation, you will be prompted to set the username and password for the PostgreSQL superuser (default is `postgres`).
4. After installation, open **DBeaver** or any other SQL client to connect to the database.
5. Start the PostgreSQL service:
   - Open the **Services** application from the Start menu.
   - Find `PostgreSQL` in the list, right-click, and select **Start**.

### Connecting to the Database using DBeaver
1. Download and install **DBeaver** from the [official website](https://dbeaver.io/download/).
2. Open DBeaver and click on the **New Database Connection** button.
3. Select **PostgreSQL** from the list of database drivers and click **Next**.
4. Enter the connection details:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `your_database_name`
   - **Username**: `postgres`
   - **Password**: `your_password`
5. Click **Finish** to establish the connection.

## DDL Statements
To create the tables in the database, follow these steps:

1. Open DBeaver and connect to your PostgreSQL database.
2. Open a new SQL editor by clicking on the **SQL Editor** button.
3. Go to the directory cd .../DataCollectorAPI/PostgresDB/
4. Load the SQL script( `DDL_Statements.sql` ) containing the DDL statements into the editor.
5. Execute the script by clicking the **Execute SQL Script** button.


## Loading Data into the DB

To load data into the database, use the provided SQL scripts( `cd .../DataCollectorAPI/PostgresDB/DML_Statements.sql` ) to load data from CSV files into the respective tables.

### Loading CSV Data into PostgreSQL Database

#### Loading data into tables by executing the command inside the file `DML_Statements.sql` some of the commands are shown below: 

```sql
COPY CVE(cve_id, sourceIdentifier, published, lastModified, vulnStatus)
FROM 'path/to/cve.csv' DELIMITER '|' CSV HEADER;

COPY Descriptions(id, cve_id, lang, value) 
FROM 'path/to/descriptions.csv' DELIMITER '|' CSV HEADER;

....
``` 


#### After uploading the data, next step is to Run FlaskApi to query data data from the database For detailed instructions, refer to the next README file: [FlaskApi README](../FlaskApi/README.md). 
