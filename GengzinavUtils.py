#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# Hello world - 西蒙.科泽斯 这是“向编程之神所称颂的传统咒语，愿他帮助并保佑你更好的学习这门语言

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class GengzinavUtils():
    """
    工具类
    """

    def trim(self,s):
        '''
        取出首尾前后的空格
        :param s:
        :return:
        '''
        for i in range(len(s)):
            if s[0] ==' ':
                s = s[1:]
        for k in range(len(s)):
            if s[-1] == ' ':
                s = s[:-1]
        return s
