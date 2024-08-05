# About FlaskApi


## Table of Contents
- [Introduction](#introduction)
- [How to Setup/ Use the API](#??)
- [API Documentation](#api-documentation)
- 


## Introduction
This README file provides a comprehensive overview of the RestApi, including how to set up and use the API, including starting the server and making requests. API Documentation: Document your API’s endpoints, including request methods, parameters, and sample responses.


## How to Setup/ Use the API
In order to setup and use the API follow these steps:
1- Go to the directory cd ../DataCollectorAPI/FlaskApi/ 
2- python -m venv venv 
3- .\venv\Scripts\Activate   # fow windows 11 on cmd
4- python.exe -m pip install --upgrade pip 
5- pip install -r requirements.txt 
6- python .\app.py




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


