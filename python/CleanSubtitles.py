import re
import sys

from python.DccUtils import get_subfolders, get_files, parse_args


def main(argv):
    args = parse_args(argv)
    path = args["path"]

    ans = input("WARNING: this will remove all non-readable lines in ALL files in folder & nested folders in {}\n Continue? (y/n)".format(path));
    while ans != "y" and ans != "n":
        ans = input("WARNING: this will remove all non-readable lines in ALL files in folder & nested folders in {}\n Continue? (y/n)".format(path));
    if ans == "n":
        print("CleanSubtitles canceled")
        return

#    subfolders = get_subfolders(path)
#
#    for subfolder in subfolders:
#        for filepath in get_files(subfolder):
#            print("doing {}".format(filepath))
#            with open(filepath, 'r', encoding='utf-8') as file:
#                try:
#                    lines = file.readlines()
#                except:
#                    continue
#            with open(filepath, 'w', encoding='utf-8') as file:
#                for line in lines:
#                    if re.search("[一-龠]+|[ぁ-ゔ]+|[ァ-ヴー]+|[a-zA-Z]+|[ａ-ｚＡ-Ｚ]+|[々〆〤]+", line):
#                        file.write(line)
#                    else:
#                        pass


if __name__ == "__main__":
    print("CleanSubtitles started")
    main(sys.argv[1:])
    print("CleanSubtitles successfully executed")
