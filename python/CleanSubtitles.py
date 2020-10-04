import re
import sys

from python.DccUtils import get_subfolders, get_files, parse_args


def main(argv):
    args = parse_args(argv)
    path = args["path"]
    subfolders = get_subfolders(path)

    for subfolder in subfolders:
        for filepath in get_files(subfolder):
            print("doing {}".format(filepath))
            with open(filepath, 'r', encoding='utf-8') as file:
                try:
                    lines = file.readlines()
                except:
                    continue
            with open(filepath, 'w', encoding='utf-8') as file:
                for line in lines:
                    if re.search("[一-龠]+|[ぁ-ゔ]+|[ァ-ヴー]+|[a-zA-Z]+|[ａ-ｚＡ-Ｚ]+|[々〆〤]+", line):
                        file.write(line)
                    else:
                        pass


if __name__ == "__main__":
    print("CleanSubtitles started")
    main(sys.argv[1:])
    print("CleanSubtitles successfully executed")
