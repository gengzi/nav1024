#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# Hello world - 西蒙.科泽斯 这是“向编程之神所称颂的传统咒语，愿他帮助并保佑你更好的学习这门语言


#导入 requests
import  requests
from MysqlHelper import *
# 使用 lxml 的 etree 库
from lxml import etree
import time
from requests.adapters import HTTPAdapter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from GengzinavDAO import *

# 爬取规则
# (1) 链接中必须携带http
# (2) 使用xpath 解析
#     //a/@href
#     //a/text()
#

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
#超时时间
TIMEOUTS = 10
#重试次数
MAX_RETRIES = 2
utils = GengzinavUtils()
dao = GengzinavDAO()



"""
加载导航页面
"""
def loadPage(url):
    response = requests.get(url,headers = headers)
    htmlResponse = response.text
    isnav = 0
    ispaqu = 0
    #解析
    etreeText = etree.HTML(htmlResponse)
    links = etreeText.xpath('//a')
    for link in links:
        linkhref = link.xpath('@href')
        linktext = link.xpath('text()')
        if len(linkhref) >0 :
            linkhref = linkhref[0]
        if len(linktext) >0 :
            linktext = linktext[0]
        # linktext = str(linktext).decode('unicode_escape').encode("UTF-8")
        #清洗链接
        if "http" in linkhref :
            if "导航" in linktext :
                isnav = 1
            else:
                isnav = 0
            #存入到数据库
            dao.saveLinkInfo(linktext,linkhref,isnav,ispaqu)
        else:
            continue;


def loadPageVer2(url):
    '''
    加载该页面中所有的链接，删除重复的，链接必须包含 http 字段。
    :param url:
    :return:
    '''
    response = requests.get(url,headers = headers)
    htmlResponse = utils.setCharester(response)
    isnav = 0
    ispaqu = 0
    #解析
    etreeText = etree.HTML(htmlResponse)

    links = etreeText.xpath('//a')
    for link in links:
        linkhref = link.xpath('@href')
        linktext = link.xpath('text()')
        if len(linkhref) >0 :
            linkhref = linkhref[0]
        if len(linktext) >0 :
            linktext = linktext[0]
        # linktext = str(linktext).decode('unicode_escape').encode("UTF-8")
        #清洗链接
        print("不符合："+linkhref)
        if "http" in linkhref :
            # 查询该链接是否存在与数据库中
            count = dao.selectlinkIsExit(utils.trim(linkhref))
            # 转换一下，求个数
            count = count[0][0]
            if count == 0:
                if "导航" in linktext :
                    isnav = 1
                else:
                    isnav = 0
                #存入到数据库
                print("存放到数据库-link:"+linkhref)
                dao.saveLinkInfo(linktext,linkhref,isnav,ispaqu)
            else:
                continue
        else:
            continue




def isInvalid(NoIsError_links):
    '''
    链接是否失效,重试两次，超时时间是10秒
    :param uri: 链接
    :return:
    '''
    for onelink in NoIsError_links:
        # print("link"+str(onelink[1]))
        # print("id" + str(onelink[0]))
        id = str(onelink[0])
        print("正在测试link："+str(onelink[1]))
        try:
            session = requests.Session()
            session.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
            session.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
            response = session.get(str(onelink[1]),headers=headers,timeout = TIMEOUTS)

            if response.status_code == 200 :
                #拿到当前网站的title
                htmlinfo = utils.setCharester(response)
                etreeText = etree.HTML(htmlinfo)
                title = etreeText.xpath('//title/text()')
                if len(title) > 0:
                    strtitle = str(title[0])

                #修改表数据,标识链接可以访问
                print("修改id：" + str(onelink[0])+"的iserror为：1,标题："+strtitle)
                dao.updateIsInvalidAndTitle(id,1,strtitle)
            else:
                print("设置id：" + str(onelink[0]) + "的iserror为：2")
                dao.updateIsInvalid(id, 2)
                #不是继续循环
                continue
        except Exception, e:
            print("link:"+str(onelink[1])+"出错")
            print("设置id：" + str(onelink[0]) + "的iserror为：2")
            dao.updateIsInvalid(id, 2)
            print(e)
            continue



def loadNavLink():
    '''
    加载是 导航的链接
    :return:
    '''
    #获取现在还没有测试过，是否能够访问的链接
    NoIsError_links = dao.selectlinkNoIsError()
    # TODO 暂时屏蔽
    if len(NoIsError_links) > 0:
        #把所有链接测试一遍
        isInvalid(NoIsError_links)
    #查询是导航链接的，没有爬取过的，能够访问成功的
    IsNav_links = dao.selectlinkNoIsnav()
    if len(IsNav_links) > 0:
        for IsNav_link in IsNav_links:
            #加载
            uri = str(IsNav_link[1])
            id = str(IsNav_link[0])
            # print("link:"+uri)
            # print("id:" + id)
            print("load链接:"+uri)
            try:
                loadPageVer2(str(IsNav_link[1]))
            except Exception,e:
                print("link:" + str(IsNav_link[1]) + "出错")
                print(e)
                continue
            #将该链接爬取状态修改为 爬取
            dao.updateIspaqu(id=id,ispaqu=1)
        #继续执行
        loadNavLink()
    else:
        print("都执行完毕了！！！")



"""
    ########
    version1.0 简单的示例，一个文件搞定
    抓取导航页面的所有链接
    ########
     version1.1
     分层处理  
     解析“导航”的关键字，爬取导航里面的内容
     并加上当前链接是否失效，判断ping 是否会超时
     QAQ： 发现一个特点，有些网站在白天是访问不进去的，然后到了网上12点，就可以访问了。
    ########
     version1.2  更新，修复bug
     标题出现乱码，在读取链接页面时，能访问成功的话，获取tilte重新设置
     发现查找到的链接有些不是 1024 网站。
     --- 出现一个问题： 编码问题，解析出来的文本报错
"""

if __name__ == "__main__":

    #loadPage("http://apart.cf/")
    loadNavLink()
