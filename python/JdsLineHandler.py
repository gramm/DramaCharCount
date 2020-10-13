import os
import sys

from python import DccUtils
from python.DccUtils import parse_args
from python.JdsDatabase import JdsDatabase
from python.JdsLine import JdsLine


class JdsLineHandler:
    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()

    def reset(self):
        return self.db.reset_lines()

    def read_lines(self):
        subfolders = DccUtils.get_subfolders(self.args["path"])
        line_id = 0
        lines = []
        for subfolder in subfolders:
            drama = JdsDatabase.get_drama(os.path.basename(subfolder))
            for filepath in DccUtils.get_files(subfolder):
                with open(filepath, encoding='utf-8') as file:
                    for line in file.readlines():
                        lines.append(JdsLine(uid=line_id, drama_uid=drama.uid, value=line))
                        line_id += 1
            self.db.push_lines(lines)
            lines.clear()


if __name__ == "__main__":
    print("{} started".format(__file__))

    jds_line_handler = JdsLineHandler(sys.argv[1:])

    jds_line_handler.reset()

    jds_line_handler.read_lines()

    print("{} ended".format(__file__))
