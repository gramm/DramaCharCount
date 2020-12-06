import cProfile
import csv
import os
import sys
import time

from python import DccUtils, settings
from python.DccUtils import parse_args
from python.JdsDatabase import JdsDatabase
from python.classes.JdsDrama import JdsDrama

if __name__ == "__main__":
    print("{} started".format(__file__))
    start_time = time.perf_counter()

    if settings.enable_profiler:
        pr = cProfile.Profile()
        pr.enable()

    args = parse_args(sys.argv[1:])
    db = JdsDatabase()
    kanji_info_results = db.get_kanji_info_raw()
    kanji_count_results = db.get_kanji_count_raw()

    with open(settings.csv_path_kanji, mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['kanji', 'count', 'freq', 'cumul_freq', 'drama_freq', 'episode_freq', 'jdpt', 'jdpt_pos', 'jouyou', 'jouyou_pos']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')
        rows = {}
        writer.writeheader()
        for result in kanji_info_results:
            if result['flag'] is not 1:
                continue
            row = {}
            rows[result['kanji_uid']] = row
            row['kanji'] = chr(result['kanji_uid'])
            row['jouyou'] = result['jouyou']
            row['jouyou_pos'] = result['jouyou_pos']
            row['jdpt'] = result['jdpt']
            row['jdpt_pos'] = result['jdpt_pos']
            row['freq'] = result['freq']
            row['cumul_freq'] = result['cumul_freq']
            row['drama_freq'] = result['drama_freq']
            row['episode_freq'] = result['episode_freq']

        for result in kanji_count_results:
            if result['drama_uid'] is not JdsDatabase.get_merged_drama().uid:
                continue
            if result['kanji_uid'] not in rows:
                continue
            row = rows[result['kanji_uid']]
            row['count'] = result['count']

        writer.writerows(rows.values())

    print("{} ended in {:2.2f}".format(__file__, (time.perf_counter() - start_time)))

    if settings.enable_profiler:
        pr.disable()
        pr.print_stats(sort="cumulative")
