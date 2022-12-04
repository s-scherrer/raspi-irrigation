#!/usr/bin/env python3

# Script that reads data from the arduino and writes it to database

from datetime import datetime, timezone
import logging
import math
import os
import psycopg2
import random
import serial
import time

from writer import DataWriter
from reader import DataReader


def make_bool(b):
    if isinstance(b, bool):
        return b
    elif isinstance(b, (int, float)):
        return b != 0
    elif isinstance(b, str):
        return b not in ["0", "false", "False"]
    else:
        raise ValueError(f"Unknown format for bool: {b}")


# set up logging
TEST_WEBAPP = make_bool(os.getenv("TEST_WEBAPP", False))
if TEST_WEBAPP:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO
logging.basicConfig(
    filename="arduino_comm.log",
    level=loglevel,
)
logging.debug(f"TEST_WEBAPP = {TEST_WEBAPP}")

# we wait some time so all the other processes have some time to start
time.sleep(20)

# tty of the arudino serial connection, e.g. /dev/ttyACM0
ARDUINO_SERIAL_TTY = os.getenv("ARDUINO_SERIAL_TTY")

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
            x = random.normalvariate(0, 1)
            t = datetime.now(timezone.utc)
            y = math.sin(2 * math.pi * t.timestamp() / 3600) + 0.2 * x
            logging.debug(t.isoformat())
            writer.write_measurement(t, y, 1)
            writer.write_measurement(t, 100 * (2 - y) / 2, 2)
            time.sleep(10)
    else:
        logging.debug("Running in production mode.")
        # default baudrate of Arduino is 9600
        # after 3600 seconds = 1 hour without data, stop
        with serial.Serial(ARDUINO_SERIAL_TTY, 9600, timeout=3600) as ser:
            # the first line is "Finished setup!" and should be skipped
            ser.readline()
            reader = DataReader(ser)
            while reader.readline():
                t = datetime.now(timezone.utc)
                id, val = reader.obs
                writer.write_measurement(t, val, id)
except:
    raise
finally:
    conn.close()
    logging.info("Done!")
