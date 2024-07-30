import logging
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import config.cpe_conf as cpe_info
from utils.data_fetcher import fetch_data
from utils.data_processor import process_cpe_info
from utils.csv_writer import update_csv_files
from utils.file_manager import delete_file


def main():
    load_dotenv()

    now = datetime.now()
    formatted_current_date = now.strftime("%Y-%m-%d_%H_%M_%S")

    here = os.path.abspath(os.path.dirname(__file__))
    logfile_name = f"data_retrieval_cpes_{formatted_current_date}.log"
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

    api_params = cpe_info.Params['CPE_INFO']
    api_url = api_params['URL']
    csv_files = cpe_info.Params['STORE_DATA']
    headers = cpe_info.Params['HEADERS']
    data_folder = cpe_info.Params['SUB_DIR']['dir_name']

    delete_file(csv_files, data_folder)

    api_key = os.getenv('CVE_API_KEY')

    extract_data(api_url, api_key, csv_files, process_cpe_info, headers, data_folder)
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
        items = data.get('products', [])
        if not items:
            break

        processed_data = process_function(items)
        update_csv_files(processed_data, csv_files, headers, data_folder)
        
        start_index += 10000
        log.info(f"total results : {total_results}")
        log.info(f"start_index : {start_index}")
        time.sleep(6)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"unexpected {err}, {type(err)}=")