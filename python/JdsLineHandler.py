import cProfile
import concurrent.futures
import os
import sys
import time

from mysql.connector import Error
from python import DccUtils, settings
from python.DccUtils import parse_args, exception
from python.JdsDatabase import JdsDatabase
from python.classes.JdsLine import JdsLine


class JdsLineHandler:
    """
    Read all lines in the provided folder, assign them a unique uid and push the result in the database
    The drama must have been loaded to the database before (via JdsDramaHandler)
    """

    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()
        self.episode_to_uid = {}

    def reset(self):
        return self.db.reset_lines()

    def line_ref_worker(self, subfolder):
        lines = []
        drama = self.db.get_drama(os.path.basename(subfolder))
        print("read_lines for drama {}".format(drama.uid))
        subfolders = DccUtils.get_subfolders(self.args["path"])
        for filepath in DccUtils.get_files(subfolder):
            filename = os.path.basename(filepath)
            with open(filepath, encoding='utf-8') as file:
                try:
                    for line in file.readlines():
                        try:
                            lines.append(JdsLine(uid=0, drama_uid=drama.uid, value=line, episode_uid=self.episode_to_uid[filename]))
                        except Exception as e:
                            exception(e)
                except Exception as e:
                    exception(e)
        return lines

    def read_lines(self):
        line_id = 0
        subfolders = DccUtils.get_subfolders(self.args["path"])
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            try:
                futures = {}
                for subfolder in subfolders:
                    futures[subfolder] = executor.submit(self.line_ref_worker, subfolder)
                for future in concurrent.futures.as_completed(futures.values()):
                    lines = future.result()
                    for line in lines:
                        line.uid = line_id
                        line_id += 1
                    self.db.push_lines(lines)
            except Error as e:
                exception(e)

    def setup(self):
        results = self.db.get_episodes_raw()
        for result in results:
            self.episode_to_uid[result['name']] = result['episode_uid']


if __name__ == "__main__":
    print("{} started".format(__file__))
    start_time = time.perf_counter()

    if settings.enable_profiler:
        pr = cProfile.Profile()
        pr.enable()

    jds_line_handler = JdsLineHandler(sys.argv[1:])

    jds_line_handler.reset()

    jds_line_handler.setup()

    jds_line_handler.read_lines()

    print("{} ended in {:2.2f}".format(__file__, (time.perf_counter() - start_time)))

    if settings.enable_profiler:
        pr.disable()
        pr.print_stats(sort="cumulative")
