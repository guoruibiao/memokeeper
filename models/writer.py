# coding: utf8
import os
import const
import conf.conf as app_conf
from datetime import date
from library.word_spliter import extract_keywords, _load_stopwords
from library.encrypt import md5
from collections import defaultdict

# storage bucket at lifecycle
bucket = defaultdict()


def _get_date():
    return date.today().strftime("%Y%m%d")


def _generate_fullname(folder, keywords):
    length = len(keywords)
    if length <= 0:
        return "", const.ERROR_FILENAME_KEYWORD_EMPTY
    limited_keyowrds = []
    for index in range(0, app_conf.MAX_KEYOWRDS_IN_FILEPATH if length > app_conf.MAX_KEYOWRDS_IN_FILEPATH else length):
        limited_keyowrds.append(keywords[index])

    filename = str(app_conf.KEYWORD_SEPARATOR).join(limited_keyowrds)
    fullname = "{}/{}{}".format(folder, filename, app_conf.FILENAME_SUFFIX)

    if len(fullname) >= app_conf.MAX_FILEPATH_LENGTH:
        return "", const.ERROR_PATH_LENGTH_TOOLONG
    return fullname, None


def write(content):
    if content == "":
        return
    keywords, tmp_words = [], extract_keywords(content)
    if len(tmp_words) <= 0:
        return

    # filter illegal words
    stop_words = _load_stopwords()
    for keyword in tmp_words:
        append_flag = True
        for sw in stop_words:
            if sw in keyword:
                append_flag = False
                break
        if append_flag:
            keywords.append(keyword)
    print("final keywords=", keywords)
    md5_sum = md5(content)
    if md5_sum in bucket.keys():
        return

    date_str = _get_date()
    folder = ("{}{}" if app_conf.STORAGE_FOLDER.endswith("/") else "{}/{}"). \
        format(app_conf.STORAGE_FOLDER, date_str)
    if not os.path.exists(folder):
        os.makedirs(folder)

    fullname, err = _generate_fullname(folder, keywords)
    print(fullname, ", err= ", err)
    with open(fullname, "a") as f:
        f.write(content)
        f.close()

    # update keywords
    _update_keywords(folder, fullname)

    bucket[md5_sum] = 1
    return


def _update_keywords(folder, fullname):
    content = ""
    with open(fullname, "r") as f:
        content = "\n".join(f.readlines())
        f.close()

    keywords = extract_keywords(content)
    newname, err = _generate_fullname(folder, keywords)
    if err != None:
        return
    os.rename(fullname, newname)
