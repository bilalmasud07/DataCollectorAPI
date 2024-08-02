import logging
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import config.cve_conf as cve_info
from utils.data_fetcher import fetch_data
from utils.data_processor import process_cve_data
from utils.csv_writer import update_csv_files
from utils.file_manager import delete_file


def main():
    load_dotenv()

    now = datetime.now()
    formatted_current_date = now.strftime("%Y-%m-%d_%H_%M_%S")

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

    delete_file(csv_files, data_folder)

    api_key  = os.getenv('CVE_API_KEY')

    extract_data(api_url, api_key, csv_files, process_cve_data, headers, data_folder)
    log.info("finished main()")


def extract_data(api_url, api_key, csv_files, process_function, headers, data_folder):
    log = logging.getLogger(__name__)
    start_index = 0
    total_results = 0

    while start_index <= total_results:
        data = fetch_data(api_url, api_key, start_index)

        if data is None:
            break
        total_results = data.get('totalResults', 0)
        items = data.get('vulnerabilities', [])
        if not items:
            break

        processed_data = process_function(items)
        update_csv_files(processed_data, csv_files, headers, data_folder)
        log.info(f"Data added to the csv files")
        
        start_index += 2000 # maximum data to be fetched, defined by the API
        log.info(f"total results : {total_results}")
        log.info(f"start_index : {start_index}")
        time.sleep(6) # recommended sleep time between each call by the API


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"unexpected {err}, {type(err)}=")