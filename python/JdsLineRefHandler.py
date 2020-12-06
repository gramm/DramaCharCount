import concurrent.futures
import sys
import time

from mysql.connector import Error

from python import settings
from python.DccUtils import parse_args, exception
from python.classes.JdsChar import JdsChar
from python.JdsDatabase import JdsDatabase
import cProfile


class JdsLineRefHandler:
    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()
        self.lines_by_drama = None

    def reset(self):
        return self.db.reset_line_refs()

    def line_ref_worker(self, drama):
        """
        threaded worker that build references of characters with lines.
        requires drama,lines to be in the DB beforehand
        :param drama:
        :return:
        """
        lines = {}  # key = char, value = [] of line_uid
        if drama.uid not in self.lines_by_drama:
            return {}
        jds_lines = self.lines_by_drama[drama.uid]
        print("start line_ref_worker for {}".format(drama.value))
        start_time = time.perf_counter()
        for jds_line in jds_lines:
            for char in jds_line.value:
                try:
                    if char not in lines:
                        lines[char] = []
                    lines[char].append(jds_line.uid)
                except Exception as e:
                    exception(e)

        jds_chars = {}
        for char in lines:
            new_char = JdsChar.from_drama(char, drama.uid)
            new_char.add_line_refs(lines[char])
            jds_chars[char] = new_char
        if "\n" in lines:
            del lines[JdsChar("\n")]
            print("Deleted \\n")
        run_time = time.perf_counter() - start_time
        print("stop line_ref_worker for {} with {} chars in {}".format(drama.value, len(lines), run_time))
        return jds_chars

    def do_line_ref(self):
        dramas = self.db.get_all_dramas()
        self.lines_by_drama = self.db.get_all_lines_by_drama()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            while len(dramas) > 0:
                try:
                    futures = {}
                    for drama in dramas:
                        if drama.kanji_line_ref_ok is 1:
                            print("kanji_line_ref_ok TRUE -> {} skipped".format(drama.uid))
                            dramas.remove(drama)
                            continue

                        futures[drama] = executor.submit(self.line_ref_worker, drama)
                        dramas.remove(drama)
                        if len(futures) > 10:
                            break
                    for future in concurrent.futures.as_completed(futures.values()):
                        chars = future.result()
                        self.db.push_chars_to_line(chars)
                except Error as e:
                    exception(e)


if __name__ == "__main__":
    print("{} started".format(__file__))

    if settings.enable_profiler:
        pr = cProfile.Profile()
        pr.enable()

    jds_line_ref_handler = JdsLineRefHandler(sys.argv[1:])

    # uncomment to clear all line associations
    jds_line_ref_handler.reset()

    jds_line_ref_handler.do_line_ref()

    print("{} ended".format(__file__))

    if settings.enable_profiler:
        pr.disable()
        pr.print_stats(sort="cumulative")