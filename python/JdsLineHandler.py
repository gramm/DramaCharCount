import sys
import concurrent.futures

from python import DccUtils
from python.DccUtils import parse_args
from python.JdsDatabase import JdsDatabase


class JdsLineHandler:
    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()

    @staticmethod
    def __read_lines_worker(subfolder, position):
        print("{} {}".format(subfolder, position))
        pass

    def connect(self):
        return self.db.connect(self.args)

    def reset(self):
        return self.db.reset_lines()

    def read_lines(self):
        subfolders = DccUtils.get_subfolders(self.args["path"])
        line_id = 0
        lines = {}
        for subfolder in subfolders:
            for filepath in DccUtils.get_files(subfolder):
                with open(filepath, encoding='utf-8') as file:
                    for line in file.readlines():
                        lines[line_id] = line
                        line_id += 1
            self.db.push_lines(lines)
            lines.clear()

    def get_lines_for_drama(self, drama):



if __name__ == "__main__":
    print("{} started".format(__file__))

    jds_line_handler = JdsLineHandler(sys.argv[1:])

    jds_line_handler.connect()

    jds_line_handler.reset()

    jds_line_handler.read_lines()

    print("{} ended".format(__file__))
