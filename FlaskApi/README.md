# About FlaskApi


## Table of Contents
- [Introduction](#introduction)
- [How to Setup and Use the API](#how-to-setup-and-use-the-api)
- [API Documentation](#api-documentation)
- [Explanation of Code Logic](#explanation-of-code-logic)


## Introduction
This README file provides a comprehensive overview of the RestApi, including how to set up and use the API, including starting the server and making requests. API Documentation: Document your API’s endpoints, including request methods, parameters, and sample responses.


## How to Setup and Use the API

In order to set up and use the API, follow these steps:

1. Go to the directory:
    ```bash
    cd ../DataCollectorAPI/FlaskApi/
    ```

2. Create a `.env` file inside that directory and add the following line:
    ```
    DATABASE_URL='postgresql+psycopg://username:password@localhost:5432/database_name'
    ```
    Replace `username`, `password`, and `database_name` with your actual PostgreSQL credentials and database name.

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
    This command creates a new virtual environment named `venv` in your project directory.

4. Activate the virtual environment:
    ```bash
    .\venv\Scripts\Activate
    ```
    This command activates the virtual environment, allowing you to install packages and run the app in an isolated environment.

5. Upgrade pip:
    ```bash
    python.exe -m pip install --upgrade pip
    ```
    This command upgrades pip, the Python package installer, to the latest version.

6. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
    This command installs all the dependencies listed in the `requirements.txt` file.

7. Run the application:
    ```bash
    python .\app.py
    ```
    This command starts the Flask application.


## API Documentation

### Overview

This API allows querying data stored in the database with flexible filtering, pagination, and sorting capabilities. It supports various operators for filtering and handles pagination efficiently.

### Endpoints

#### 1. Query Data from Database

##### URL
[GET /query](http://127.0.0.1:5000/query?table=CVE&page=1&per_page=100)

##### Description

Queries data from the specified table in the database with optional filters and pagination.

##### Parameters

- `table` (string, required): The name of the table to query.
- `page` (integer, optional): The page number for pagination. Default is 1.
- `per_page` (integer, optional): The number of results per page. Default is 100.
- Additional query parameter can be used as filters. Supported operator:
  - `=` for equality (e.g., `column=value`)


##### Sample Requests

1. **Simple Query**:
[GET /query?table=CVE&page=1&per_page=10](http://127.0.0.1:5000/query?table=CVE&page=1&per_page=100)


2. **Equality Filter**:
[http://127.0.0.1:5000/query?table=CVE&vulnStatus=Modified&page=1&per_page=100](http://127.0.0.1:5000/query?table=CVE&vulnStatus=Modified&page=1&per_page=100)



#### 2. Retrieve Data by Specific Parameter (Product_ID)

##### URL
[GET /Product_ID=A132CA24-0C21-4D60-BB30-98ACD8D15D6E](http://127.0.0.1:5000/Product_ID=A132CA24-0C21-4D60-BB30-98ACD8D15D6E)


#### Sample Request
```bash
http://127.0.0.1:5000/Product_ID=A132CA24-0C21-4D60-BB30-98ACD8D15D6E
```

#### Description
Retrieves data based on the specified Product ID.

#### Parameters
- `Product_ID` (UUID, required): The ID of the CPE to retrieve.

#### Sample Answer

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


### 3. Analytical Questions

#### For all the analytical quetions data is not being used which is collected after 05-01-2024. 

#### 3.1 Severity Distribution

##### URL
[GET /severity_distribution](http://127.0.0.1:5000/severity_distribution)


##### Description
Provides the count of vulnerabilities for different severity levels.

##### Sample Request
```bash
http://127.0.0.1:5000/severity_distribution
```

##### Sample Answer

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

#### 3.2 Worst Products and Platforms
##### URL
[GET /worst_products_platforms](http://127.0.0.1:5000/worst_products_platforms)


##### Description
Finds out the worst products and platforms with the most number of known vulnerabilities.

##### Sample Request
```bash
http://127.0.0.1:5000/worst_products_platforms
```

##### Sample Answer

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


#### 3.3 Top 10 Vulnerabilities with the Highest Impact
##### URL
[GET /top_vulnerabilities_highest_impact](http://127.0.0.1:5000/top_vulnerabilities_highest_impact)


##### Description
Lists the top 10 vulnerabilities that have the highest impact.

##### Sample Request
```bash
http://127.0.0.1:5000/top_vulnerabilities_highest_impact
```

##### Sample Answer

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


#### 3.4 Top 10 Vulnerabilities with the Highest Impact
##### URL
[GET /top_vulnerabilities_highest_exploitability](http://127.0.0.1:5000/top_vulnerabilities_highest_exploitability)


##### Description
Lists the top 10 vulnerabilities that have the highest impact.

##### Sample Request
```bash
http://127.0.0.1:5000/top_vulnerabilities_highest_exploitability
```

#### Sample Answer


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


#### 3.5 Top 10 Attack Vectors Used
##### URL
[GET /top_attack_vectors](http://127.0.0.1:5000/top_attack_vectors)


##### Description
Lists the top 10 attack vectors used.

##### Sample Request
```bash
http://127.0.0.1:5000/top_attack_vectors
```

##### Sample Answer

```json
[
    {
        "attackVector": "NETWORK",
        "total_count": 192731
    },
    {
        "attackVector": "LOCAL",
        "total_count": 51870
    },
    {
        "attackVector": "ADJACENT_NETWORK",
        "total_count": 6558
    },
    {
        "attackVector": "PHYSICAL",
        "total_count": 1927
    }
]
```


#### 4. Match Strings by Criteria ID

##### URL
[GET /match_strings/DD38B1D2-5860-4CE2-A33F-BAF27C2F3B34](http://127.0.0.1:5000/matchCriteriaId=DD38B1D2-5860-4CE2-A33F-BAF27C2F3B34)

##### Description
Retrieves match strings based on the specified match criteria ID.

##### Parameters
matchCriteriaId (UUID, required): The match criteria ID to retrieve.


##### Sample Request
```bash
http://127.0.0.1:5000/matchCriteriaId=DD38B1D2-5860-4CE2-A33F-BAF27C2F3B34
```

##### Sample Answer
```json
{
    "totalResults": 1,
    "format": "NVD_CPEMatchString",
    "version": "2.0",
    "timestamp": "2024-08-06T01:22:06.556",
    "matchStrings": [
        {
            "matchString": {
                "matchCriteriaId": "DD38B1D2-5860-4CE2-A33F-BAF27C2F3B34",
                "criteria": "cpe:2.3:o:cisco:ios:12.1\\(14\\)e7:*:*:*:*:*:*:*",
                "lastModified": "2019-06-17T09:16:33.960",
                "cpeLastModified": "2019-07-22T16:37:38.133",
                "created": "2019-06-17T09:16:33.960",
                "status": "Active",
                "matches": [
                    {
                        "cpeName": "cpe:2.3:o:cisco:ios:12.1\\(14\\)e7:*:*:*:*:*:*:*",
                        "cpeNameId": "39BF6108-A2CE-41D9-BF76-F30DD64219CD"
                    }
                ]
            }
        }
    ]
}
```


## Explanation of Code Logic

This project is a Flask-based API designed to provide detailed information about Common Vulnerabilities and Exposures (CVEs). It uses SQLAlchemy for database interactions, Flask-Caching for caching, and various other utilities to enhance the functionality and performance of the API.

### Project Structure

The project is organized as follows:

- **app.py**: Entry point of the Flask application.
- **app/**: Contains application-related code.
  - **routes/**: Contains the route definitions.
  - **models/**: Contains the SQLAlchemy models.
  - **\_\_init\_\_.py**: Initializes the Flask application.
  - **config.py**: Configuration settings for the application.


### Code Explanation

### app.py

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

```

This is the main entry point of the application. It imports and creates an instance of the Flask application and runs it in debug mode if executed directly.


### app/__init__.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from app.config import Config
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})

def create_app():
    load_dotenv()  # Load environment variables from .env file
    
    here = os.path.abspath(os.path.dirname(__file__))
    parent_directory = os.path.dirname(here)

    # Get current UTC time
    current_utc_time = datetime.now(timezone.utc)
    formatted_time = current_utc_time.strftime('%Y%m%d')

    # Define log file path
    logfile_name = f"Vuln_app_{formatted_time}.log"
    logfile_path = os.path.join(parent_directory, 'logs', logfile_name)

    # Initialize logging
    logging.basicConfig(
        filename=logfile_path, level=logging.INFO, 
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    log = logging.getLogger(__name__)
    
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cache.init_app(app)
    
    with app.app_context():
        from app.routes import register_routes
        register_routes(app, db)

    return app

```
This file initializes the Flask application. It sets up logging, loads environment variables, and registers routes.


### app/config.py

```python
import os
from dotenv import load_dotenv

# Explicitly specify the path to the .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'

```
This file contains the configuration settings for the Flask application, including database URI and secret key.


### app/models.py

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class CVE(db.Model):
    __tablename__ = 'cve'
    cve_id = db.Column(db.String(255), primary_key=True)
    sourceidentifier = db.Column(db.String(255), nullable=False)
    published = db.Column(db.TIMESTAMP, nullable=False)
    lastmodified = db.Column(db.TIMESTAMP, nullable=False)
    vulnstatus = db.Column(db.String(255), nullable=False)

# Other models follow similar structure

```
This file defines the SQLAlchemy models representing the database schema.


### app/routes.py

```python
from flask import jsonify, Response, request
from app.models import CVE, CVSSMetric, CpeMatch, Nodes, Configurations, SourceType, Matches, MatchString, CPE, Titles, Descriptions, Weaknesses, WeaknessesDescriptions
import logging
from datetime import datetime, timezone
import json
from sqlalchemy import func, and_
from collections import defaultdict
from uuid import UUID
from app import cache

# Custom JSON Encoder to handle datetime and UUID
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)

def register_routes(app, db):
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "Welcome to the CVE API!"}), 200

    @cache.cached(timeout=60, key_prefix='cpe_%s')
    @app.route('/Product_ID=<uuid:cpename_id>', methods=['GET'])
    def get_cpe(cpename_id):
        try:
            # Query to join necessary tables
            cpe_data = db.session.query(
                CPE,
                Titles
            ).outerjoin(Titles, Titles.cpenameid == CPE.cpenameid)\
            .filter(CPE.cpenameid == cpename_id)\
            .all()
            logging.info(f"cpe_data: {cpe_data}")
            if not cpe_data:
                return jsonify({"error": f"CPE with ID {cpename_id} not found."}), 404

            # Create the cpe object
            cpe = cpe_data[0][0]
            titles = [title for cpe, title in cpe_data if title]

            data = {
                "totalResults": len(cpe_data),
                "format": "NVD_CPE",
                "version": "2.0",
                "timestamp": formatted_time,
                "products": [
                    {
                        "cpe": {
                            "deprecated": cpe.deprecated,
                            "cpeName": cpe.cpename,
                            "cpeNameid": str(cpe.cpenameid).upper(),
                            "lastModified": cpe.lastmodified.isoformat(timespec='milliseconds') if cpe.lastmodified else None,
                            "created": cpe.created.isoformat(timespec='milliseconds') if cpe.created else None,
                            "titles": [
                                {"title": title.title} for title in titles
                            ]
                        }
                    }
                ]
            }
            response = Response(json.dumps(data), mimetype='application/json')
            return response, 200
        except Exception as e:
            logging.error(f"Error in get_cpe: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    # Similar structure for other routes
    @cache.cached(timeout=60, key_prefix='cve_%s')
    @app.route('/CVE_ID=<string:cveid>', methods=['GET'])
    def get_cve(cveid):
        # Code for handling CVE details

    @cache.cached(timeout=60)
    @app.route('/severity_distribution', methods=['GET'])
    def severity_distribution():
        # Code for handling severity distribution

    @cache.cached(timeout=60)
    @app.route('/worst_products_platforms', methods=['GET'])
    def worst_products_platforms():
        # Code for handling worst products platforms

    @cache.cached(timeout=60)
    @app.route('/top_vulnerabilities_highest_impact', methods=['GET'])
    def top_vulnerabilities_highest_impact():
        # Code for handling top vulnerabilities with highest impact

    @cache.cached(timeout=60)
    @app.route('/top_vulnerabilities_highest_exploitability', methods=['GET'])
    def top_vulnerabilities_highest_exploitability():
        # Code for handling top vulnerabilities with highest exploitability

    @app.route('/top_attack_vectors', methods=['GET'])
    def top_attack_vectors():
        # Code for handling top attack vectors

    @app.route('/matchCriteriaId=<uuid:matchcriteriaid>', methods=['GET'])
    def match_strings(matchcriteriaid):
        # Code for handling match strings

    @app.route('/query', methods=['GET'])
    def query_database():
        # Code for handling custom database queries

    logging.info("Routes have been registered successfully.")


```

This file defines the routes for the Flask application. Each route handles specific endpoints and provides relevant data in JSON format.


## Comments
- Ensure that the .env file is correctly set up with the necessary environment variables such as DATABASE_URI.
- The logging setup in \_\_init\_\_.py ensures that all logs are saved in a structured manner with timestamps.
- Caching is used extensively to improve the performance of the API by storing responses for a specified duration.

# Conclusion
This Flask API provides comprehensive data on CVEs, leveraging SQLAlchemy for database interactions and Flask-Caching for performance optimization. The project is well-structured and modular, making it easy to maintain and extend.
