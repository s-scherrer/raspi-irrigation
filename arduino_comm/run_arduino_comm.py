#!/usr/bin/env python3

# Script that reads data from the arduino and writes it to database

from datetime import datetime, timezone
import numpy as np
import os
from pathlib import Path
import psycopg2
import time

from writer import DataWriter


workdir = Path(__file__).resolve().parent


# connect to database
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
conn = psycopg2.connect(
    f"dbname={POSTGRES_DB} user={POSTGRES_USER}"
    f" password={POSTGRES_PASSWORD} host={POSTGRES_HOST}"
)

writer = DataWriter(conn)

TEST_WEBAPP = os.getenv("TEST_WEBAPP")
if TEST_WEBAPP:
    print("Running in test mode.")
    print("This means random data is generated.")

    for i in range(5):
        print(i)
        writer.write_measurement(
            datetime.now(timezone.utc),
            np.random.randn(),
            1
        )
        time.sleep(5)
else:
    print("Running in production mode.")

conn.close()
print("Done!")
