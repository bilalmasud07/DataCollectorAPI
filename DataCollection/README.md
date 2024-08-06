
## About DataCollection

This part will collect the data from three APIs.

Follow the steps below to run DataCollection scripts (total 3):

1. **Request an API Key**:
   - Request an API key using the link below:
     [NVD API Key Request](https://nvd.nist.gov/developers/request-an-api-key)
   - The API key will be sent to the provided email address.

2. **Open the Repository in a Code Editor**:
   - Open the repository in your preferred code editor (e.g., VSCode).

3. **Create an `.env` File**:
   - Create an `.env` file under the directory `.../DataCollection/.env`
   - Store the API key like this and save it:
     ```plaintext
     CVE_API_KEY='PASTE API KEY HERE'
     ```

4. **Scripts to Run**:
   - There are 3 scripts to run to fetch data from the APIs. The APIs used are:
     - The CVE API is used to easily retrieve information on a single CVE or a collection of CVEs from the NVD.
       
       ```sh
       https://services.nvd.nist.gov/rest/json/cves/2.0
       ```
     - The CPE API is used to easily retrieve information on a single CPE record or a collection of CPE records from the Official CPE Dictionary.
       
       ```sh
       https://services.nvd.nist.gov/rest/json/cpes/2.0
       ```
     - The CPE Match Criteria API is used to easily retrieve the complete list of valid CPE Match Strings.
       
       ```sh
       https://services.nvd.nist.gov/rest/json/cpematch/2.0
       ```

5. **Run the First Script**:
   - Open a terminal in the editor, go to the directory `.../DataCollectorAPI/DataCollection/`, and install first all requirement then run the first script named `cves_data_retrieval.py` to retrieve data about CVEs:
     
     ```sh
     pip install -r requirements.txt  
     python ./cves_data_retrieval.py
     ```
   - After running the script, it will log all activities in the file `.../DataCollectorAPI/DataCollection/logs/data_retrieval_cves_{current_timestamp}.log`. The script collects data in chunks and processes it into CSV files under the directory specified in `.../DataCollectorAPI/DataCollection/config/cve_conf.py`. Each CSV file represents a table, with attributes defined in the `cve_conf.py` file.

6. **Run the Second Script**:
   - Change the current directory path in the terminal to `.../DataCollectorAPI/DataCollection/` and run the second script named `cpes_data_retrieval.py` to retrieve data about CPEs:
     
     ```sh
     python ./cpes_data_retrieval.py
     ```
   - The script logs all activities in the file `.../DataCollectorAPI/DataCollection/logs/data_retrieval_cpes_{current_timestamp}.log`. It collects data in chunks and processes it into CSV files under the directory specified in `.../DataCollectorAPI/DataCollection/config/cpe_conf.py`. Each CSV file represents a table, with attributes defined in the `cpe_conf.py` file.

7. **Run the Third Script**:
   - Change the current directory path in the terminal to `.../DataCollectorAPI/DataCollection/` and run the third script named `cpe_match_data_retrieval.py` to retrieve data about valid CPE Match Strings:
     
     ```sh
     python ./cpe_match_data_retrieval.py
     ```
   - The script logs all activities in the file `.../DataCollectorAPI/DataCollection/logs/data_retrieval_cpe_match_{current_timestamp}.log`. It collects data in chunks and processes it into CSV files under the directory specified in `.../DataCollectorAPI/DataCollection/config/cpe_match_conf.py`. Each CSV file represents a table, with attributes defined in the `cpe_match_conf.py` file.
  
**Note**: Steps 5, 6, and 7 can be run simultaneously to generate all data/CSV files at the same time.

8. **Proceed to the Next Part**:
   - Once all three scripts have finished running, proceed to the second part, which involves creating the database and uploading data into the database. For detailed instructions, refer to the next README file: [PostgresDB README](../PostgresDB/README.md).


# DataCollection Project

This repository is designed to collect and process CVE (Common Vulnerabilities and Exposures), CPE (Common Platform Enumeration), and CPE Match data. The data is fetched from an API, processed, and stored in CSV files for further analysis.

## Folder Structure

- **DataCollection**
  - **cves_data_retrieval.py**: Script for retrieving CVE data.
  - **cpes_data_retrieval.py**: Script for retrieving CPE data.
  - **cpe_match_data_retrieval.py**: Script for retrieving CPE Match data.
  - **config/**
    - **cve_conf.py**: Configuration for CVE data retrieval.
    - **cpe_conf.py**: Configuration for CPE data retrieval.
    - **cpe_match_conf.py**: Configuration for CPE Match data retrieval.
  - **logs/**: Directory for log files.
  - **cve_csv_data/**: Directory for storing CVE CSV data.
  - **cpe_csv_data/**: Directory for storing CPE CSV data.
  - **cpematch_csv_data/**: Directory for storing CPE Match CSV data.
  - **utils/**
    - **csv_writer.py**: Utility for writing data to CSV files.
    - **data_fetcher.py**: Utility for fetching data from the API.
    - **data_processor.py**: Utility for processing fetched data.
    - **file_manager.py**: Utility for managing files (e.g., deleting old CSV files).

## Scripts and Utilities

### cves_data_retrieval.py

This script retrieves CVE data from an API, processes it, and stores it in CSV files. It handles logging and file management.


#### Main Function

```python
def main():
    load_dotenv()  # Load environment variables from a .env file.

    now = datetime.now()
    formatted_current_date = now.strftime("%Y-%m-%d_%H_%M_%S")

    # Set up logging
    here = os.path.abspath(os.path.dirname(__file__))
    logfile_name = f"data_retrieval_cves_{formatted_current_date}.log"
    logfile_path = os.path.join(here, "logs", logfile_name)
    logfile_handler = logging.FileHandler(logfile_path)
    logging.basicConfig(
        format="{asctime}:{levelname}:{name}: {message}",
        style="{",
        level=logging.INFO,
        handlers=(logfile_handler, logging.StreamHandler()),
    )
    log = logging.getLogger(__name__)
    log.info("starting main()")

    api_params = cve_info.Params['CVE_INFO']
    api_url = api_params['URL']
    csv_files = cve_info.Params['STORE_DATA']
    headers = cve_info.Params['HEADERS']
    data_folder = cve_info.Params['SUB_DIR']['dir_name']

    delete_file(csv_files, data_folder)  # Delete existing CSV files.

    api_key  = os.getenv('CVE_API_KEY')  # Retrieve API key from environment variables.

    extract_data(api_url, api_key, csv_files, process_cve_data, headers, data_folder)
    log.info("finished main()")
```

#### Extract Data Function

```python
def extract_data(api_url, api_key, csv_files, process_function, headers, data_folder):
    log = logging.getLogger(__name__)
    start_index = 0
    total_results = 0

    while start_index <= total_results:
        data = fetch_data(api_url, api_key, start_index)  # Fetch data from the API.

        if data is None:
            break
        total_results = data.get('totalResults', 0)
        items = data.get('vulnerabilities', [])
        if not items:
            break

        processed_data = process_function(items)  # Process the fetched data.
        update_csv_files(processed_data, csv_files, headers, data_folder)  # Write processed data to CSV files.
        log.info(f"Data added to the csv files")
        
        start_index += 2000  # Maximum data to be fetched, defined by the API.
        log.info(f"total results : {total_results}")
        log.info(f"start_index : {start_index}")
        time.sleep(6)  # Recommended sleep time between each call by the API.
```

#### cpes_data_retrieval.py
This script retrieves CPE data, processes it, and stores it in CSV files. It is similar to cves_data_retrieval.py but tailored for CPE data.

#### cpe_match_data_retrieval.py
This script retrieves CPE Match data, processes it, and stores it in CSV files. It is similar to cves_data_retrieval.py but tailored for CPE Match data.

#### utils/csv_writer.py
This utility writes processed data to CSV files.

```python
def write_to_csv(file_path, data, headers):
    log = logging.getLogger(__name__)
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='|')
        if not file_exists:
            writer.writerow(headers)
        writer.writerows(data)

def update_csv_files(data, csv_files, headers, data_folder):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    for key, rows in data.items():
        file_path = os.path.join(parent_dir, data_folder, csv_files[key])
        write_to_csv(file_path, rows, headers[key])
```


#### utils/data_fetcher.py
This utility fetches data from the API.

```python
def fetch_data(api_url, api_key, start_index=0):
    log = logging.getLogger(__name__)
    params = {'startIndex': start_index}
    headers = {"apiKey": api_key}

    try:
        response = requests.get(api_url, headers=headers, params=params)
        log.info(f"Response: {response}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        log.error(f"HTTP error occurred: {http_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        log.error(f"Request failed: {req_err}")
        raise
```

#### utils/data_processor.py
This utility processes the fetched data.

#### utils/file_manager.py
This utility handles file operations such as deleting old CSV files.

#### Configuration Files
Configuration files store the parameters required for each data retrieval script. They are located in the config/ directory and contain information such as API URLs, headers, and CSV file paths.

- **config/cve_conf.py:** Configuration for CVE data retrieval.
- **config/cpe_conf.py:** Configuration for CPE data retrieval.
- **config/cpe_match_conf.py:** Configuration for CPE Match data retrieval.

### Logs
Log files are stored in the logs/ directory. Each script generates a log file with a timestamp in its name.

### CSV Data
CSV files are stored in separate directories for each type of data:

- **cve_csv_data/:** Contains CSV files for CVE data.
- **cpe_csv_data/:** Contains CSV files for CPE data.
- **cpematch_csv_data/:** Contains CSV files for CPE Match data.


