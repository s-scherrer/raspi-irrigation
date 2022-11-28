import logging
import struct


class DataReader:
    def __init__(self, ser):
        self.ser = ser

    def readline(self):
        line = self.ser.readline()
        try:
            self.obs = self.parse_line(line)
        except struct.error:
            logging.info(f"Invalid line read: {line}")
        return True

    @staticmethod
    def parse_line(line):
        # the first to bytes correspond to a unsigned short obs id
        id = struct.unpack("H", line[0:2])[0]
        # the next 4 bytes are the value as float
        val = struct.unpack("f", line[2:6])[0]
        return id, val
