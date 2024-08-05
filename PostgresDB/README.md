This part includes:
* Data Modelling
* Setting up Postgres database, DDL statements
* Adding data(csv files) into Postgres database


# Vulnerability Management Database

## Table of Contents
- [Introduction](#introduction)
- [ETL Design](#etl-design)
- [Data Model Explanation](#data-model-explanation)
- [Columns and Tables Explanation](#columns-and-tables-explanation)
- [Data Model Diagram](#data-model-diagram)

## Introduction
This README file provides a comprehensive overview of the vulnerability management database, including ETL design, data model, and detailed explanation of tables and columns. This database is designed to store information about Common Vulnerabilities and Exposures (CVEs), their descriptions, related metrics, configurations, and other relevant data.

## ETL Design
The ETL (Extract, Transform, Load) process for this database involves the following steps:

### Extract
- **Source**: Data is extracted from various vulnerability data feeds, such as the National Vulnerability Database (NVD) and other trusted sources.
- **Data Types**: The extracted data includes CVE information, descriptions, metrics, weaknesses, configurations, and match criteria.

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
