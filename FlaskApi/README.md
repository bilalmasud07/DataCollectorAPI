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

### Sample Request
```bash
`GET /Product_ID=<uuid:cpename_id>`
`http://127.0.0.1:5000/Product_ID=A132CA24-0C21-4D60-BB30-98ACD8D15D6E`
```

### Description
Retrieves data based on the specified CPE ID.

### Parameters
- `Product_ID` (UUID, required): The ID of the CPE to retrieve.

### Sample Request
```bash
GET /Product_ID=bae41d20-d4af-4af0-aa7d-3bd04da402a7
http://127.0.0.1:5000/Product_ID=A132CA24-0C21-4D60-BB30-98ACD8D15D6E
```

### Sample Answer

```json
{
    "totalResults": 1,
    "format": "NVD_CPE",
    "version": "2.0",
    "timestamp": "2024-08-05T18:24:43.058",
    "products": [
        {
            "cpe": {
                "deprecated": true,
                "cpeName": "cpe:2.3:a:rsa:bsafe_crypto-c:-:*:*:*:*:*:*:*",
                "cpeNameid": "A132CA24-0C21-4D60-BB30-98ACD8D15D6E",
                "lastModified": "2021-12-15T14:02:52.940",
                "created": "2007-08-23T21:05:57.937",
                "titles": [
                    {
                        "title": "RSA BSAFE Crypto-C"
                    }
                ]
            }
        }
    ]
}
```


## 3. Analytical Questions

### 3.1 Severity Distribution

#### URL
`GET /severity_distribution`

`http://127.0.0.1:5000/severity_distribution`


#### Description
Provides the count of vulnerabilities for different severity levels.

#### Sample Request
```bash
[GET /severity_distribution](http://127.0.0.1:5000/severity_distribution)
```

### Sample Answer

```json
[
    {
        "baseseverity": "CRITICAL",
        "total_severities": 22005
    },
    {
        "baseseverity": "HIGH",
        "total_severities": 90393
    },
    {
        "baseseverity": "LOW",
        "total_severities": 7950
    },
    {
        "baseseverity": "MEDIUM",
        "total_severities": 98428
    }
]
```

### 3.2 Worst Products and Platforms
#### URL
`GET /worst_products_platforms`

`http://127.0.0.1:5000/worst_products_platforms`


#### Description
Finds out the worst products and platforms with the most number of known vulnerabilities.

#### Sample Request
```bash
[GET /severity_distribution](http://127.0.0.1:5000/severity_distribution)](http://127.0.0.1:5000/worst_products_platforms)
```

### Sample Answer

```json
[
    {
        "product": "cpe:2.3:o:apple:mac_os_x:-:*:*:*:*:*:*:*",
        "total_known_vulnerabilities": 3585
    },
    {
        "product": "cpe:2.3:o:microsoft:windows_server_2016:-:-:*:*:standard:*:x86:*",
        "total_known_vulnerabilities": 2659
    },
    {
        "product": "cpe:2.3:o:microsoft:windows_server_2016:-:-:*:*:essentials:*:x86:*",
        "total_known_vulnerabilities": 2659
    },
    {
        "product": "cpe:2.3:o:microsoft:windows_server_2016:-:-:*:*:essentials:*:x64:*",
        "total_known_vulnerabilities": 2659
    },
    {
        "product": "cpe:2.3:o:microsoft:windows_server_2016:-:-:*:*:datacenter:*:x86:*",
        "total_known_vulnerabilities": 2659
    },
    {
        "product": "cpe:2.3:o:microsoft:windows_server_2016:-:-:*:*:datacenter:*:x64:*",
        "total_known_vulnerabilities": 2659
    },
    {
        "product": "cpe:2.3:o:microsoft:windows_server_2016:-:-:*:*:multipoint_premium_server:*:x86:*",
        "total_known_vulnerabilities": 2659
    },
    {
        "product": "cpe:2.3:o:microsoft:windows_server_2016:-:-:*:*:multipoint_premium_server:*:x64:*",
        "total_known_vulnerabilities": 2659
    },
    {
        "product": "cpe:2.3:o:microsoft:windows_server_2016:-:-:*:*:standard:*:x64:*",
        "total_known_vulnerabilities": 2659
    },
    {
        "product": "cpe:2.3:o:microsoft:windows_server_2016:-:*:*:*:*:*:*:*",
        "total_known_vulnerabilities": 2659
    }
]
```


### 3.3 Top 10 Vulnerabilities with the Highest Impact
#### URL
GET /top_vulnerabilities_highest_impact


#### Description
Lists the top 10 vulnerabilities that have the highest impact.

#### Sample Request
```bash
[http://127.0.0.1:5000/top_vulnerabilities_highest_impact](http://127.0.0.1:5000/top_vulnerabilities_highest_impact)
```

### Sample Answer

```json
[
    {
        "cve_id": "CVE-1999-0002",
        "impactScore": 10
    },
    {
        "cve_id": "CVE-1999-0003",
        "impactScore": 10
    },
    {
        "cve_id": "CVE-1999-0005",
        "impactScore": 10
    },
    {
        "cve_id": "CVE-1999-0006",
        "impactScore": 10
    },
    {
        "cve_id": "CVE-1999-0008",
        "impactScore": 10
    },
    {
        "cve_id": "CVE-1999-0009",
        "impactScore": 10
    },
    {
        "cve_id": "CVE-1999-0011",
        "impactScore": 10
    },
    {
        "cve_id": "CVE-1999-0014",
        "impactScore": 10
    },
    {
        "cve_id": "CVE-1999-0018",
        "impactScore": 10
    },
    {
        "cve_id": "CVE-1999-0022",
        "impactScore": 10
    }
]
```


### 3.4 Top 10 Vulnerabilities with the Highest Impact
#### URL
GET /top_vulnerabilities_highest_exploitability


#### Description
Lists the top 10 vulnerabilities that have the highest impact.

#### Sample Request
```bash
[http://127.0.0.1:5000/top_vulnerabilities_highest_exploitability](http://127.0.0.1:5000/top_vulnerabilities_highest_exploitability)
```

### Sample Answer


```json
[
    {
        "cve_id": "CVE-1999-0001",
        "exploitabilityscore": 10
    },
    {
        "cve_id": "CVE-1999-0002",
        "exploitabilityscore": 10
    },
    {
        "cve_id": "CVE-1999-0003",
        "exploitabilityscore": 10
    },
    {
        "cve_id": "CVE-1999-0004",
        "exploitabilityscore": 10
    },
    {
        "cve_id": "CVE-1999-0005",
        "exploitabilityscore": 10
    },
    {
        "cve_id": "CVE-1999-0006",
        "exploitabilityscore": 10
    },
    {
        "cve_id": "CVE-1999-0007",
        "exploitabilityscore": 10
    },
    {
        "cve_id": "CVE-1999-0008",
        "exploitabilityscore": 10
    },
    {
        "cve_id": "CVE-1999-0009",
        "exploitabilityscore": 10
    },
    {
        "cve_id": "CVE-1999-0010",
        "exploitabilityscore": 10
    }
]
```



