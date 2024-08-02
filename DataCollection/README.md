About DataCollection

This part will collect the data from three API's.

Follow below steps to follow run datacollection scripts(total 3)


1- Request an API KEY, using this link below:
https://nvd.nist.gov/developers/request-an-api-key

API KEY will be sent to the provided email address.

2- Open the reposity in the code editor(vscode etc)

3- Create an .env file under directory .../DataCollection/.env
store the API KEY like this exactly and save it.
`CVE_API_KEY='PASTE API KEY HERE'`

4- There are 3 scripts to run to fetch data form the API's.
these are the 3 API's being used:
* The CVE API is used to easily retrieve information on a single CVE or a collection of CVE from the NVD
  `ttps://services.nvd.nist.gov/rest/json/cves/2.0`
* The CPE API is used to easily retrieve information on a single CPE record or a collection of CPE records from the Official CPE Dictionary
  `https://services.nvd.nist.gov/rest/json/cpes/2.0`
* The CPE Match Criteria API is used to easily retrieve the complete list of valid CPE Match Strings
  `https://services.nvd.nist.gov/rest/json/cpematch/2.0`

5- Open a terminal in the editor go the the directory cd `.../DataCollectorAPI/DataCollection/` and run 1st script named `"cves_data_retrieval.py"` to retrieve data     about CVE. 
  `python .\cves_data_retrieval.py`
  After running the script, it will show all the log in file(`.../DataCollectorAPI/DataCollection/logs/`) `"data_retrieval_cves_{current_timestamp}.log"` that its    collectiong the data in chunks and after processing it adds into the csv files under directory .../DataCollectorAPI/DataCollection/config/cve_conf.py 
  It will create different csv files and add data into each files. Each csv file represents a table. 
  The information about each table attributes are defined in `.../DataCollectorAPI/DataCollection/config/cve_conf.py` file along with what API is being used.

6- Run 2nd script to fetch all the record of the CPE, under the directory `.../DataCollectorAPI/DataCollection/` and run second script named `"cpes_data_retrieval.py"` to retrieve data about CVE. Run below command to run the script.
  `python ./cpes_data_retrieval.py`
  After running the script, it will show all the log in file(`.../DataCollectorAPI/DataCollection/logs/`) `"data_retrieval_cpes_{current_timestamp}.log"` that its    collectiong the data in chunks and after processing it adds into the csv files under directory `.../DataCollectorAPI/DataCollection/config/cpe_conf.py` 
  It will create different csv files and add data into each files. Each csv file represents a table. 
  The information about each table attribute are defined in `.../DataCollectorAPI/DataCollection/config/cpe_conf.py` file along with what API is being used.
  
7- Run 3rd script to fetch all the record of the valid CPE Match Strings. Under the directory `.../DataCollectorAPI/DataCollection/`, run third script named `"cpe_match_data_retrieval.py"` to retrieve data about CVE. Run below command to run the script.
  `python ./cpe_match_data_retrieval.py`
  After running the script, it will show all the log in file (`.../DataCollectorAPI/DataCollection/logs/`) `"data_retrieval_cpe_match_{current_timestamp}.log"`     
  that its collectiong the data in chunks and after processing it adds into the csv files under directory 
  `.../DataCollectorAPI/DataCollection/config/cpe_match_conf.py` It will create different csv files and add data into each files. Each csv file represents a table. 
  The information about each table attribute are defined in `.../DataCollectorAPI/DataCollection/config/cpe_match_conf.py` file along with what API is being used.

Step 5, 6, and 7 can be run simentaneuosly as well to generate all data/csv files at the same time.

8- When all the three scripts finished running then follow the next 2nd part which to create database and upload data into database.

8- cd .\FlaskApi\
3- python -m venv venv
4- .\venv\Scripts\Activate
5- python.exe -m pip install --upgrade pip
6- pip install -r requirements.txt
7- python .\app.py
8- 
