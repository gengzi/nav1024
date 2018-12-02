#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# Hello world - 西蒙.科泽斯 这是“向编程之神所称颂的传统咒语，愿他帮助并保佑你更好的学习这门语言
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from GengzinavDAO import *





if __name__ == "__main__":
    dao = GengzinavDAO()
    # dao.updateIsInvalid(id="871",isInvalid="1");

    # list = dao.selectlinkNoIsError()
    # for one in list:
    #     print(str(one[0])+":"+one[1])

    link = dao.selectlinkIsExit("http://www.zxjp.xyz/")
    print(link[0][0])

