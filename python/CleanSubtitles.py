import getopt
import re
import sys

from python.DccUtils import get_subfolders, get_files


def parse_args(argv):
    ret_dict = {
        "path": ""
    }
    try:
        opts, args = getopt.getopt(argv, "pa", ["path="])
    except getopt.GetoptError as err:
        print("Could not parse program arguments")
        print(str(err))  # will print something like "option -a not recognized"
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-pa', '--path'):
            ret_dict["path"] = arg
            print("path = {}".format(ret_dict["path"]))
        else:
            print("Unknown argument {}".format(opt))
            sys.exit(2)

    for key, value in ret_dict.items():
        if not value:
            print("Missing command line arguments {}".format(key))
            sys.exit(2)
    return ret_dict


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
                    #if re.match(u"[ぁ-んァ-ンー一-龯a-zA-Zａ-ｚＡ-Ｚ[\uFF21-\uFF3A][\uFF41-\uFF5A][\uFF66-\uFF9D]]", line):
                    if re.search("[一-龠]+|[ぁ-ゔ]+|[ァ-ヴー]+|[a-zA-Z]+|[ａ-ｚＡ-Ｚ]+|[々〆〤]+", line):
                        file.write(line)
                    else:
                        pass
                        #print("removing {}".format(line))




if __name__ == "__main__":
    print("CleanSubtitles started")
    main(sys.argv[1:])
    print("CleanSubtitles successfully executed")
