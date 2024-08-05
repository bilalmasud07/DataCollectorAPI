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

comment out below commands where necessary

1- Go to the directory cd ../DataCollectorAPI/FlaskApi/ 

2- Create a .env file inside that directory and write below line
DATABASE_URL='postgresql+psycopg://username:password@localhost:5432/database_name'

replace then your username, passowrd, database name which you have set in part two

explain what below command does
2- python -m venv venv 

explain what below command does
3- .\venv\Scripts\Activate   # fow windows 11 on cmd

4- python.exe -m pip install --upgrade pip 

explain what below command does
5- pip install -r requirements.txt 

explain what below command does
6- python .\app.py



# Flask API Documentation

## Overview

This API allows querying data stored in the database with flexible filtering, pagination, and sorting capabilities. It supports various operators for filtering and handles pagination efficiently.

## Endpoints

### 1. Query Data from Database

#### URL

`GET /query`

#### Description

Queries data from the specified table in the database with optional filters and pagination.

#### Parameters

- `table` (string, required): The name of the table to query.
- `page` (integer, optional): The page number for pagination. Default is 1.
- `per_page` (integer, optional): The number of results per page. Default is 100.
- Additional query parameter can be used as filters. Supported operator:
  - `=` for equality (e.g., `column=value`)


#### Sample Requests

1. **Simple Query**:

GET /query?table=CVE&page=1&per_page=10
[http://127.0.0.1:5000/query?table=CVE&page=1&per_page=100](http://127.0.0.1:5000/query?table=CVE&page=1&per_page=100)




2. **Equality Filter**:

GET /query?table=CVE&vulnstatus=Modified&page=1&per_page=10
[http://127.0.0.1:5000/query?table=CVE&vulnStatus=Modified&page=1&per_page=100](http://127.0.0.1:5000/query?table=CVE&vulnStatus=Modified&page=1&per_page=100)



### 2. Retrieve Data by Specific Parameter (Product_ID)

### URL
`GET /Product_ID=<uuid:cpename_id>`
`http://127.0.0.1:5000/Product_ID=A132CA24-0C21-4D60-BB30-98ACD8D15D6E`


### Description
Retrieves data based on the specified CPE ID.

### Parameters
- `Product_ID` (UUID, required): The ID of the CPE to retrieve.

### Sample Request
```bash
GET /Product_ID=bae41d20-d4af-4af0-aa7d-3bd04da402a7
http://127.0.0.1:5000/Product_ID=A132CA24-0C21-4D60-BB30-98ACD8D15D6E
