# coding: utf8

import hashlib

def md5(content):
    hl = hashlib.md5()
    hl.update(content.encode("utf8"))
    return hl.hexdigest()