"""
Writer class for retrieved data.
"""

import logging


class DataWriter:
    """Writes measured data to database."""

    def __init__(self, conn):
        """
        Parameters
        ----------
        conn : database connection
        """
        self.conn = conn
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * from public.irrigation_app_measurement"
                " ORDER BY id DESC"
            )
            last_measurement = cur.fetchone()
            if last_measurement is None:
                self.last_id = -1
            else:
                self.last_id = last_measurement[0]
            logging.debug(f"Last ID = {self.last_id}")

    def write_measurement(self, time, value, obs_id):
        """
        Writes single measurement to database.

        Parameters
        ----------
        time : datetime.datetime
            Measurement time
        value : float
            Measured value
        obs_id : int
            ID of the observable that was measured. See
            `webapp/irrigation_app/fixtures/observables.json` for available
            values.
        """
        cur = self.conn.cursor()
        with self.conn.cursor() as cur:
            logging.debug(
                f"Inserting with ID = {self.last_id+1}, value = {value},"
                f" observation ID = {obs_id}."
            )
            cur.execute(
                "INSERT INTO public.irrigation_app_measurement"
                " (id, time, value, observable_id) VALUES (%s, %s, %s, %s)",
                (self.last_id + 1, time, value, obs_id)
            )
            self.last_id += 1
            logging.debug("Done")
