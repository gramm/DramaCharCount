import struct


class JdsChar:
    def __key(self):
        return self.value

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, JdsChar):
            return self.__key() == other.__key()
        return NotImplemented

    def __init__(self, value):
        self.value = value
        self.uid = ord(value)
        self.lines = set()
        self.drama_uid = None

    def add_line_ref(self, line_uid):
        self.lines.add(line_uid)
