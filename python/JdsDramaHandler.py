import cProfile
import os
import sys
import time

from python import DccUtils, settings
from python.DccUtils import parse_args
from python.JdsDatabase import JdsDatabase
from python.classes.JdsDrama import JdsDrama


class JdsDramaHandler:
    """
    Find all the drama in the given folder (i.e. top level subfolders), assign a uid and push then to the database
    """

    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()

    def reset(self):
        return self.db.reset_dramas()

    def read_dramas(self):
        subfolders = DccUtils.get_subfolders(self.args["path"])
        dramas = [self.db.get_merged_drama()]
        for subfolder in subfolders:
            dramas.append(JdsDrama(len(dramas), os.path.basename(subfolder)))
        self.db.push_dramas(dramas)

    def read_episodes(self):
        episodes = {}
        subfolders = DccUtils.get_subfolders(self.args["path"])
        for subfolder in subfolders:
            for filepath in DccUtils.get_files(subfolder):
                episodes[len(episodes)] = os.path.basename(filepath)
        self.db.push_episodes(episodes)


if __name__ == "__main__":
    print("{} started".format(__file__))
    start_time = time.perf_counter()

    if settings.enable_profiler:
        pr = cProfile.Profile()
        pr.enable()

    jds_drama_handler = JdsDramaHandler(sys.argv[1:])

    jds_drama_handler.reset()

    jds_drama_handler.read_dramas()
    jds_drama_handler.read_episodes()

    print("{} ended in {:2.2f}".format(__file__, (time.perf_counter() - start_time)))

    if settings.enable_profiler:
        pr.disable()
        pr.print_stats(sort="cumulative")
