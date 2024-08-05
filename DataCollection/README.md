
8- cd .\FlaskApi\
3- python -m venv venv
4- .\venv\Scripts\Activate
5- python.exe -m pip install --upgrade pip
6- pip install -r requirements.txt
7- python .\app.py
8- 


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
       `https://services.nvd.nist.gov/rest/json/cves/2.0`
     - The CPE API is used to easily retrieve information on a single CPE record or a collection of CPE records from the Official CPE Dictionary.
       `https://services.nvd.nist.gov/rest/json/cpes/2.0`
     - The CPE Match Criteria API is used to easily retrieve the complete list of valid CPE Match Strings.
       `https://services.nvd.nist.gov/rest/json/cpematch/2.0`

5. **Run the First Script**:
   - Open a terminal in the editor, go to the directory `.../DataCollectorAPI/DataCollection/`, and run the first script named `cves_data_retrieval.py` to retrieve data about CVEs:
     ```sh
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
   - Once all three scripts have finished running, proceed to the second part, which involves creating the database and uploading data into the database.

