import os
from dotenv import dotenv_values

log_dir = dotenv_values(".env").get("LOG_FILES_DIR")
log_filename = dotenv_values(".env").get("LOG_FILE_NAME")
log_full_path = os.path.join(log_dir, log_filename)

def load_data() -> list:
    log_file = open(log_full_path, "r")
    data = log_file.readlines()
    log_file.close()
    return data
