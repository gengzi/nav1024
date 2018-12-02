#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# Hello world - 西蒙.科泽斯 这是“向编程之神所称颂的传统咒语，愿他帮助并保佑你更好的学习这门语言

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
from MysqlHelper import *
from GengzinavUtils import *

# 初始化mysql
mysql = MysqlHelper(host="123.206.30.117",user="root",passwd="111",db="1024",port=3306)

utils = GengzinavUtils()

class GengzinavDAO():

    def saveLinkInfo(self,linktext,linkhref,isnav,ispaqu):
        '''
        保存数据到数据库
        :param linktext: 链接的标题
        :param linkhref: 链接
        :param isnav: 是否为导航  默认 0
        :param ispaqu: 是否爬取了 默认 0
        :return:
        '''
        try:
            sql = "insert into navigation set   title=%s , href=%s , isnavigation=%s , ispaqu=%s , create_time=%s , update_time=%s "
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            linkparams = [utils.trim(str(linktext)), utils.trim(str(linkhref)), str(isnav), str(ispaqu),str(create_time),str(create_time)]
            mysql.insert(sql=sql,params=linkparams)
        except Exception,e:
            print("GengzinavDAO:saveLinkInfo:"+e)
            return

    def updateIsInvalid(self,id,isInvalid):
        '''
        修改链接是否失效的标识
        :param id:  数据库标识
        :param isInvalid: 是否失效  默认0
        :return:
        '''
        try:
            sql = "update navigation set iserror=%s where id=%s "
            linkparams = [str(isInvalid),str(id)]
            mysql.update(sql=sql, params=linkparams)
        except Exception, e:
            print("GengzinavDAO:updateIsInvalid"+e)
            return


    def updateReadme(self,id,readme):
        '''
        修改readme，重试次数
        :param id:  数据库标识
        :param isInvalid: 是否失效  默认0
        :return:
        '''
        try:
            sql = "update navigation set readme=%s where id=%s "
            linkparams = [str(readme),str(id)]
            mysql.update(sql=sql, params=linkparams)
        except Exception, e:
            print("GengzinavDAO:updateIsInvalid"+e)
            return


    def selectlinkNoIsError(self):
        '''
        查询现在数据中，没有检测链接是否有效的数据
        :param id:  数据库标识
        :param isInvalid: 是否失效  默认0
        :return:
        '''
        try:
            sql = "select id,href from navigation where iserror = 0"
            return mysql.get_all(sql=sql)
        except Exception, e:
            print("GengzinavDAO:selectlinkNoIsError"+e)
            return


    def selectlinkNoIsnav(self):
        '''
        查询现在数据中是导航链接的，没有爬取的，能够访问成功的。
        :param id:  数据库标识
        :param isInvalid: 是否失效  默认0
        :return:
        '''
        try:
            sql = "select id,href from navigation where iserror = 1 and ispaqu = 0 and isnavigation = 1"
            return mysql.get_all(sql=sql)
        except Exception, e:
            print("GengzinavDAO:selectlinkNoIsnav"+e)
            return

    def selectlinkIsExit(self,link):
        '''
        查询当前链接是否存在该数据库
        :param id:  数据库标识
        :param isInvalid: 是否失效  默认0
        :return:
        '''
        try:
            sql = "select count(id) from navigation where href=%s"
            linkparams = [str(link)]
            return mysql.get_all(sql=sql,params=linkparams)
        except Exception, e:
            print("GengzinavDAO:selectlinkIsExit"+e)
            return

    def updateIspaqu(self,id,ispaqu):
        '''
        修改readme，重试次数
        :param id:  数据库标识
        :param isInvalid: 是否失效  默认0
        :return:
        '''
        try:
            sql = "update navigation set ispaqu=%s where id=%s "
            linkparams = [str(ispaqu),str(id)]
            mysql.update(sql=sql, params=linkparams)
        except Exception, e:
            print("GengzinavDAO:updateIspaqu"+e)
            return