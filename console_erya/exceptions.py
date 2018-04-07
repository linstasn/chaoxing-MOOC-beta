# coding:utf-8


class SearchError(Exception):
    def __init__(self, err=''):
        Exception.__init__(self, err)
