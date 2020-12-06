class JdsChar:
    def __key(self):
        return self.uid

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        # Two JdsChar are equals if they have the same uid (i.e. binary value of Char) or the same value (i.e. same Char)
        # Therefore depending of the type of other (Char or binary value of Char) we need to compare either to self.uid or self.value
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
        self.freq = 0
        self.freq_cum = 0
        self.__count = 0
        self.__count_round = None

    @classmethod
    def from_drama(cls, value, drama):
        char = cls(value)
        char.drama_uid = drama
        return char

    def add_line_ref(self, line_uid):
        self.lines.add(line_uid)

    def add_line_refs(self, line_uids):
        self.lines.update(line_uids)

    def set_count(self, count):
        self.__count = count

    def count(self):
        return self.__count

    def count_round(self):
        count = self.__count
        if count > 10000:
            count = int(int(round(count / 10000)) * 10000)
        if count > 1000:
            count = int(int(round(count / 1000)) * 1000)
        if count > 100:
            count = int(int(round(count / 100)) * 100)
        elif count > 10:
            count = int(int(round(count / 10)) * 10)
        self.__count_round = count
        return self.__count_round

    def jdpt_to_jlpt(self):
        if self.jlpt is 0:
            return -32768
        else:
            return self.jlpt_pos - self.jdpt_pos
