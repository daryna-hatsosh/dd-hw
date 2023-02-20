from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import psycopg2
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

def create_user_counter_table():
    conn = psycopg2.connect(
            host='db',
            port=5432,
            dbname='example_db',
            user='example_user',
            password='example_password'
        )
    cur = conn.cursor()

    # Execute your Python script with any necessary SQL queries
    # Replace this with your actual script logic
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS user_counter (
        user_id SERIAL PRIMARY KEY,
        counter INTEGER,
        version INTEGER
    );
    '''
    cur.execute(create_table_query)
    conn.commit()

    # Close the database connection
    cur.close()
    conn.close()

def check_db_counter():
    conn = psycopg2.connect(
        host='db',
        port=5432,
        dbname='example_db',
        user='example_user',
        password='example_password'
    )
    cur = conn.cursor()
    # counter = cur.execute('SELECT counter FROM user_counter WHERE user_id = 1').fetchone()
    cur.execute("SELECT counter FROM user_counter WHERE user_id = 1;")
    counter = cur.fetchone()[0]

    cur.close()
    conn.close()
    return counter

def insert_in_table():
    conn = psycopg2.connect(
        host='db',
        port=5432,
        dbname='example_db',
        user='example_user',
        password='example_password'
    )
    cur = conn.cursor()

    # Check if user with user_id=1 already exists in the user_counter table
    cur.execute("SELECT EXISTS(SELECT 1 FROM user_counter WHERE user_id = 1)")
    exists = cur.fetchone()[0]

    if exists:
        # If user exists, set the counter to 0
        cur.execute("UPDATE user_counter SET counter = 0 WHERE user_id = 1")
    else:
        # If user does not exist, insert a new user with user_id=1 and counter=0
        cur.execute("INSERT INTO user_counter (user_id, counter, version) VALUES (%s, %s, %s)", (1, 0, 1))

    conn.commit()

    # Close the cursor and the database connection
    cur.close()
    conn.close()

def execute_script_in_thread():
    # python -c 'from scripts import execute_script_in_thread; execute_script_in_thread()'
    # Connect to the PostgreSQL database
    logger.info("create user_counter table if does not exist")
    create_user_counter_table()

    logger.info("set user counter in db to 0")
    insert_in_table()

    logger.info("check user counter in db")
    logger.info(f'counter: {check_db_counter()}')
    
    logger.info("execute_script in 10 threads")
    start_time = datetime.now()

    # Create a thread pool with 10 threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit the function to the thread pool 10 times
        for i in range(10):
            executor.submit(update_user_counter_lost_update)
            # executor.submit(update_user_counter_inplace_update)
            # executor.submit(update_user_counter_row_level_locking)
            # executor.submit(update_user_counter_optimistic_concurrency_control)

    end_time = datetime.now()
    
    # Calculate the difference between the start time and end time
    execution_time = end_time - start_time
    db_counter = check_db_counter()

    logger.info(f'execution time: {execution_time.total_seconds()} seconds')
    logger.info("check user counter in db")
    logger.info(f'counter: {db_counter}')

    return f'execution time: {execution_time.total_seconds()} seconds; counter: {db_counter}'

def update_user_counter_lost_update():
    # Connect to the PostgreSQL database
    logger.info("lost update: create new connection and cursor for thread")
    conn = psycopg2.connect(
        host='db',
        port=5432,
        dbname='example_db',
        user='example_user',
        password='example_password'
    )
    cur = conn.cursor()

    for i in range(10000): 
        cur.execute("SELECT counter FROM user_counter WHERE user_id = 1;")
        counter = cur.fetchone()[0]
        counter = counter + 1
        cur.execute("update user_counter set counter = %s where user_id = %s", (counter, 1))
        conn.commit()

    # Close the database connection
    cur.close()
    conn.close()

def update_user_counter_inplace_update():
    # Connect to the PostgreSQL database
    logger.info("in place update: create new connection and cursor for thread")
    conn = psycopg2.connect(
        host='db',
        port=5432,
        dbname='example_db',
        user='example_user',
        password='example_password'
    )
    cur = conn.cursor()
    
    for i in range(10000):  
        cur.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = %s", (1,))
        conn.commit()

    # Close the database connection
    cur.close()
    conn.close()

def update_user_counter_row_level_locking():
    # Connect to the PostgreSQL database
    logger.info("row level locking: create new connection and cursor for thread")
    conn = psycopg2.connect(
        host='db',
        port=5432,
        dbname='example_db',
        user='example_user',
        password='example_password'
    )
    cur = conn.cursor()
    

    for i in range(10000): 
        cur.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE;")
        counter = cur.fetchone()[0]
        counter = counter + 1
        cur.execute("update user_counter set counter = %s where user_id = %s", (counter, 1))
        conn.commit()

    # Close the database connection
    cur.close()
    conn.close()

def update_user_counter_optimistic_concurrency_control():
    # Connect to the PostgreSQL database
    logger.info("optimistic concurrency control: create new connection and cursor for thread")
    conn = psycopg2.connect(
        host='db',
        port=5432,
        dbname='example_db',
        user='example_user',
        password='example_password'
    )
    cur = conn.cursor()
    
    
    for i in range(10000):
        while True:
            cur.execute("SELECT counter, version FROM user_counter WHERE user_id = 1 FOR UPDATE")
            row = cur.fetchone()
            counter = row[0]
            version = row[1]
            counter += 1
            cur.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = 1 AND version = %s", (counter, version + 1, version))
            conn.commit()
            count = cur.rowcount
            if count > 0:
                break


    # Close the database connection
    cur.close()
    conn.close()