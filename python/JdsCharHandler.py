import concurrent.futures
import sys
import time

from mysql.connector import Error

from python import settings
from python.DccUtils import parse_args, exception
from python.classes.JdsChar import JdsChar
from python.JdsDatabase import JdsDatabase
import cProfile


class JdsCharHandler:
    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()
        self.lines_by_drama = None

    def reset(self):
        return self.db.reset_chars()

    def read_chars_worker(self, drama):
        """
        threaded worker that counts all characters for a given drama, by getting all lines from the DB and counting the char.
        requires drama,lines to be in the DB beforehand
        :param drama:
        :return:
        """
        chars = {}  # key = char, value = count
        lines = {}  # key = char, value = [] of line_uid
        if drama.uid not in self.lines_by_drama:
            return chars
        jds_lines = self.lines_by_drama[drama.uid]
        print("start read_chars_worker for {}".format(drama.value))
        start_time = time.perf_counter()
        for jds_line in jds_lines:
            for char in jds_line.value:
                try:
                    if char not in chars:
                        chars[char] = 0
                        lines[char] = []
                    chars[char] = chars[char] + 1
                    lines[char].append(jds_line.uid)
                except Exception as e:
                    exception(e)

        jds_chars = {}
        for char in chars:
            new_char = JdsChar.from_drama(char, drama.uid)
            new_char.set_count(chars[char])
            new_char.add_line_refs(lines[char])
            jds_chars[char] = new_char
        if "\n" in chars:
            del chars[JdsChar("\n")]
            print("Deleted \\n")
        run_time = time.perf_counter() - start_time
        print("stop read_chars_worker for {} with {} chars in {}".format(drama.value, len(chars), run_time))
        return jds_chars

    def read_chars(self):
        dramas = self.db.get_all_dramas()
        self.lines_by_drama = self.db.get_all_lines_by_drama()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            while len(dramas) > 0:
                try:
                    futures = {}
                    for drama in dramas:
                        if drama.kanji_ok is 1:
                            dramas.remove(drama)
                            continue

                        futures[drama] = executor.submit(self.read_chars_worker, drama)
                        dramas.remove(drama)
                        if len(futures) > 10:
                            break
                    print("starting new batch...")
                    for future in concurrent.futures.as_completed(futures.values()):
                        chars = future.result()
                        self.db.push_chars_count(chars)
                        self.db.push_chars_to_line(chars)
                        self.db.push_kanji_ok(chars)
                except Error as e:
                    exception(e)
        self.db.push_chars()

    def create_tables(self):
        self.db.create_char_tables()


if __name__ == "__main__":
    print("{} started".format(__file__))

    if settings.enable_profiler:
        pr = cProfile.Profile()
        pr.enable()

    jds_char_handler = JdsCharHandler(sys.argv[1:])

    jds_char_handler.create_tables()

    # uncomment to clear all drama count i.e. restart counting (drama, lines untouched)
    jds_char_handler.reset()

    jds_char_handler.read_chars()

    print("{} ended".format(__file__))

    if settings.enable_profiler:
        pr.disable()
        pr.print_stats(sort="cumulative")
