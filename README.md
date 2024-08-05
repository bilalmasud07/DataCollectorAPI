## About DataCollectorAPI

The aim of this project is to develop end-to-end data pipelines that span the entire process from data collection to storage, and ultimately to data retrieval through a bespoke API. The project entails interacting with an open API to gather data, storing this data in a PostgreSQL database, and creating a REST API for querying and analyzing the stored data.

To achieve this, the project will involve:

- **Data Collection**: Leveraging an open API to gather the necessary data. This involves setting up mechanisms to interact with the API and handle data extraction.
- **Data Storage**: Utilizing a PostgreSQL database to securely store the collected data. This includes designing the database schema and implementing data storage solutions to ensure efficient data management and retrieval.
- **API Development**: Developing a custom REST API using the Flask framework that will provide endpoints for querying and analyzing the stored data. This involves defining the API architecture, implementing the necessary endpoints, and ensuring the API can handle various query requests efficiently.

This project combines multiple aspects of data engineering, from initial data extraction and storage to the creation of an accessible and functional API, aiming to provide a streamlined, end-to-end data solution.



### There are three main parts inside the project:

1. Collecting the data from the APIs.
2. Designing and populating the database (schema, data loading scripts).
3. Running the REST API (Flask) to show data from the created database.

Follow these three steps sequentially:

1. **Run DataCollection Script**:
   - Complete instructions are under the directory `DataCollection` [README.md](DataCollection/README.md).

2. **Run PostgresDB Script**:
   - Complete instructions are under the directory `PostgresDB` [README.md](PostgresDB/README.md).

3. **Run FlaskApi Script**:
   - Complete instructions are under the directory `FlaskApi` [README.md](FlaskApi/README.md).
