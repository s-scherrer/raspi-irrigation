from reader import DataReader


def test_parse_line():
    line = b'\x03\x00\x00\x00\x84A\n'
    id, val = DataReader.parse_line(line)
    assert id == 3
    assert val == 16.5

    b'\x02\x00\xcd\xcczB\n'
    id, val = DataReader.parse_line(line)
    assert id == 2
    assert val == 62.70000076293945
