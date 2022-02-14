from datetime import datetime
import time

def log(path, log_string):
    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    formatted_timestamp = date_time.strftime("%d-%m-%Y %H:%M:%S")

    log_string = formatted_timestamp + "§" + log_string + "\n"

    file_out = open(path, 'a')
    file_out.write(log_string)
    file_out.close()
