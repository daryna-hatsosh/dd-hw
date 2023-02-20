import logging
from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from web.scripts import check_db_counter, create_user_counter_table, execute_script_in_thread, insert_in_table

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

message_list = []
logger.info("INFO: web booted up")

@app.get('/execute-script')
def execute_script():
    logger.info("INFO: execute-script in 10 threads started")
    result = execute_script_in_thread()
    return result

if __name__ == '__main__':
    # Run the Flask app indefinitely
    app.run(debug=True, host='0.0.0.0')