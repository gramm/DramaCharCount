import concurrent.futures
import sys

from python.DccUtils import parse_args, exception
from python.JdsChar import JdsChar
from python.JdsDatabase import JdsDatabase


class JdsCharHandler:
    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()

    def reset(self):
        return self.db.reset_chars()

    def read_chars_worker(self, drama):
        print("start read_chars_worker for {}".format(drama.value))
        chars = {}  # key = char, value = count
        jds_lines = self.db.get_lines_for_drama(drama)
        for jds_line in jds_lines:
            for char in jds_line.value:
                jds_char = JdsChar(char)
                jds_char.drama_uid = drama.uid
                try:
                    # increment count for this drama
                    if jds_char in chars:
                        chars[jds_char] = chars[jds_char] + 1
                    else:
                        chars[jds_char] = 1
                    jds_char.add_line_ref(jds_line.uid)

                except Exception as e:
                    exception(e)
        if "\n" in chars:
            del chars["\n"]
            print("Deleted \\n")
        print("stop read_chars_worker for {} with {} chars".format(drama.value, len(chars)))
        return chars

    def read_chars(self):
        dramas = self.db.get_all_dramas()

        # for drama in dramas:
        #    chars = self.read_chars_worker(drama)
        #    self.db.push_chars(chars)

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = {}
            for drama in dramas:
                futures[drama] = executor.submit(self.read_chars_worker, drama)
            for future in concurrent.futures.as_completed(futures.values()):
                chars = future.result()
                self.db.push_chars_count(chars)
        self.db.push_chars()


if __name__ == "__main__":
    print("{} started".format(__file__))

    jds_char_handler = JdsCharHandler(sys.argv[1:])

    jds_char_handler.reset()

    jds_char_handler.read_chars()

    print("{} ended".format(__file__))
