# coding:utf-8


class GlobalVar:
    __var = {}

    def add(self, *args, **kwargs):
        """
        添加全局变量
        :param kwargs:
        :return:
        """
        for x in args:
            if isinstance(x, dict):
                self.__var.update(x)
        self.__var.update(kwargs)

    def get(self, key):
        try:
            return self.__var[key]
        except KeyError:
            return None

    def remove(self, key):
        """
        删除全局变量
        :param key:
        :return:
        """
        if isinstance(key, str):
            try:
                del self.__var[key]
            except KeyError:
                pass
        elif isinstance(key, list):
            for x in key:
                try:
                    del self.__var[x]
                except KeyError:
                    pass


globalvar = GlobalVar()
