import struct
import logging


class JdsChar:
    def __key(self):
        return self.uid

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, JdsChar):
            return self.__key() == other.__key()
        elif isinstance(other, int):
            return self.__key() == other
        elif isinstance(other, str):
            return self.value == other
        return NotImplemented

    def __init__(self, value):
        self.value = value
        self.uid = ord(value)
        self.lines = set()
        self.drama_uid = None
        self.jlpt = 0
        self.jouyou = 0
        self.jdpt = 0
        self.jlpt_pos = 0
        self.jouyou_pos = 0
        self.jdpt_pos = 0
        self.flag = 0
        self.__count = 0
        self.__count_round = None

    def add_line_ref(self, line_uid):
        self.lines.add(line_uid)

    def set_count(self, count):
        self.__count = count
        if count > 10000:
            count = int(int(round(count / 10000)) * 10000)
        if count > 1000:
            count = int(int(round(count / 1000)) * 1000)
        if count > 100:
            count = int(int(round(count / 100)) * 100)
        elif count > 10:
            count = int(int(round(count / 10)) * 10)
        self.__count_round = count

    def count(self):
        return self.__count

    def count_round(self):
        return self.__count_round
