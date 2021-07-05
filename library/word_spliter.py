# coding: utf8
import os
import jieba
import conf.conf as app_conf


def extract_keywords(content):
    """
    extract keywords by word's frequency
    :param content: something in your system clipboard
    :return:
    """
    keywords = []
    if content == "":
        return keywords

    words = jieba.cut(content, cut_all=True)
    stop_words = _load_stopwords()
    data1 = {}
    for chara in words:
        if chara in stop_words:
            continue
        if len(chara) < 2:
            continue
        if chara in data1:
            data1[chara] += 1
        else:
            data1[chara] = 1
    print(data1)
    keywords = sorted(data1.items(), key=lambda x: x[1], reverse=True)

    return [item[0] for item in keywords]


def _load_stopwords():
    stopwords = []
    filepath = app_conf.STOPWORDS_PATH
    if not os.path.exists(filepath):
        return stopwords

    tmpLines = []
    with open(filepath, "r") as f:
        tmpLines = f.readlines()
        f.close()
    if len(tmpLines) > 0:
        stopwords = [word for word in tmpLines if word not in stopwords]
    return stopwords
