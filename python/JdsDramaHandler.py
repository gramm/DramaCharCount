import os
import sys

from python import DccUtils
from python.DccUtils import parse_args
from python.JdsDatabase import JdsDatabase
from python.JdsDrama import JdsDrama


class JdsDramaHandler:
    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()

    def reset(self):
        return self.db.reset_dramas()

    def read_dramas(self):
        subfolders = DccUtils.get_subfolders(self.args["path"])
        dramas = [JdsDrama(0, "--> All Dramas Together <--")]
        for subfolder in subfolders:
            dramas.append(JdsDrama(len(dramas), os.path.basename(subfolder)))
        self.db.push_dramas(dramas)


if __name__ == "__main__":
    print("{} started".format(__file__))

    jds_drama_handler = JdsDramaHandler(sys.argv[1:])

    jds_drama_handler.reset()

    jds_drama_handler.read_dramas()

    print("{} ended".format(__file__))
