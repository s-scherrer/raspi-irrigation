#!/usr/bin/env python3

# Script that reads data from the arduino and writes it to database

from datetime import datetime, timezone
import logging
import numpy as np
import os
import psycopg2
import time

from writer import DataWriter


# set up logging
TEST_WEBAPP = os.getenv("TEST_WEBAPP")
if TEST_WEBAPP:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO
logging.basicConfig(
    filename="arduino_comm.log",
    level=loglevel,
)

time.sleep(20)

# connect to database
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
logging.info(f"Connecting to database {POSTGRES_DB} on {POSTGRES_HOST}")
conn = psycopg2.connect(
    f"dbname={POSTGRES_DB} user={POSTGRES_USER}"
    f" password={POSTGRES_PASSWORD} host={POSTGRES_HOST}"
)
conn.autocommit = True

try:
    logging.info("Connected to database.")
    writer = DataWriter(conn)

    if TEST_WEBAPP:
        logging.debug("Running in test mode.")
        logging.debug("This means random data is generated.")

        while True:
            x = np.random.randn()
            t = datetime.now(timezone.utc)
            y = np.sin(2*np.pi*t.timestamp()/3600) + 0.2*x
            logging.debug(t.isoformat())
            writer.write_measurement(t, y, 1)
            writer.write_measurement(t, 100*(2-y)/2, 2)
            time.sleep(10)
    else:
        logging.debug("Running in production mode.")
except:
    raise
finally:
    conn.close()
    logging.info("Done!")
