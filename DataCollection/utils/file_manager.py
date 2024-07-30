import os
import logging

def delete_file(csv_files, data_folder):
    log = logging.getLogger(__name__)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    for key, csv_file in csv_files.items():
        file_path = os.path.join(parent_dir, data_folder, csv_file)
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info(f"The existing file {file_path} has been deleted.")
        else:
            log.info(f"The file {file_path} does not exist.")
