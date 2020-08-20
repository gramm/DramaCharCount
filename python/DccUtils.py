import os


def get_subfolders(path):
    return [f.path for f in os.scandir(path) if f.is_dir()]


def get_files(path):
    retlist = []
    for root, subFolder, files in os.walk(path):
        for item in files:
            retlist.append((os.path.join(root, item)))
    return retlist


def escape_sql(sql):
    chars = ['\\', '\'', '\"']
    for c in chars:
        sql = sql.replace(c, '\\'+c)
    return sql
