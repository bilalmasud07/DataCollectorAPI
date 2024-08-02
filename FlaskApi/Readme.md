About DataCollectorAPI

The aim of this project is to develop end-to-end data pipelines that span the entire process from data collection to storage, and ultimately to data retrieval through a bespoke API. The project entails interacting with an open API to gather data, storing this data in a PostgreSQL database, and creating a REST API for querying and analyzing the stored data.

To achieve this, the project will involve:

Data Collection: Leveraging an open API to gather the necessary data. This involves setting up mechanisms to interact with the API and handle data extraction.
Data Storage: Utilizing a PostgreSQL database to securely store the collected data. This includes designing the database schema and implementing data storage solutions to ensure efficient data management and retrieval.
API Development: Developing a custom REST API using flask framework that will provide endpoints for querying and analyzing the stored data. This involves defining the API architecture, implementing the necessary endpoints, and ensuring the API can handle various query requests efficiently.
This project combines multiple aspects of data engineering, from initial data extraction and storage to the creation of an accessible and functional API, aiming to provide a streamlined, end-to-end data solution​



1- Request an API key, using this link:
https://nvd.nist.gov/developers/request-an-api-key

API key will be received via the provided email address. 

2- Download this github repository into your computer, downloading might take some time because it already include files with data in it. However it will regenarete the data as well and that's the next step.

3- Go to the downloaded repository folder 
   cd ...\DataCollectorAPI\

There are 3 main parts inside the project, one is to collect the data from the API's and another one is to use the design database(schema, data loading scripts) and the last one is run FlaskApi to shows data from the created database.

Follow these 3 steps sequentially.
1- Run DataColection script, complete instructions are under the directory DataCollection README.md file
2- Run PostgresDB script, complete instructions are under the directory PostgresDB README.md file
3- Run FlaskApi script, complete instructions are under the directory FlaskApi README.md file


