import cProfile
import os
import sys

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

    def reset(self):
        return self.db.reset_lines()

    def read_lines(self):
        subfolders = DccUtils.get_subfolders(self.args["path"])
        line_id = 0
        lines = []
        for subfolder in subfolders:
            drama = self.db.get_drama(os.path.basename(subfolder))

            print("read_lines for drama {}".format(drama.uid))
            for filepath in DccUtils.get_files(subfolder):
                with open(filepath, encoding='utf-8') as file:
                    try:
                        for line in file.readlines():
                            try:
                                lines.append(JdsLine(uid=line_id, drama_uid=drama.uid, value=line))
                                line_id += 1
                            except Exception as e:
                                exception(e)
                    except Exception as e:
                        exception(e)

            self.db.push_lines(lines)
            lines.clear()


if __name__ == "__main__":
    print("{} started".format(__file__))

    if settings.enable_profiler:
        pr = cProfile.Profile()
        pr.enable()

    jds_line_handler = JdsLineHandler(sys.argv[1:])

    jds_line_handler.reset()

    jds_line_handler.read_lines()

    print("{} ended".format(__file__))

    if settings.enable_profiler:
        pr.disable()
        pr.print_stats(sort="cumulative")
