#/usr/bin/env python
#coding: utf-8
#Author: Ezreal
#email: osatmnzn@vip.qq.com
#date: 2016.02.25
#version: 1.0

import urllib2
import urllib
import cookielib
import re
import sys
import bs4

reload(sys)
sys.setdefaultencoding('utf-8')
# print sys.getdefaultencoding()

def baiduLogin(username,password,mob=False):
    URL_BAIDU_INDEX = u'http://www.baidu.com/'
    URL_BAIDU_TOKEN = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'

    if mob == True:
        # 手机百度应用使用这个
        URL_BAIDU_LOGIN = 'http://wappass.baidu.com/passport/login'
    else:
        # 电脑百度应用使用这个
        URL_BAIDU_LOGIN = 'https://passport.baidu.com/v2/?login'

    #设置cookie，这里cookiejar可自动管理，无需手动指定
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    reqReturn = urllib2.urlopen(URL_BAIDU_INDEX)

    #获取token
    tokenReturn = urllib2.urlopen(URL_BAIDU_TOKEN)
    matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"',tokenReturn.read())
    tokenVal = matchVal.group('tokenVal')

    #构造登录请求参数，该请求数据是通过抓包获得，对应https://passport.baidu.com/v2/api/?login请求
    postData = {
        'username' : username,
        'password' : password,
        'u' : 'http://ks.baidu.com/?&lfr=1',
        # 'u' : 'http://www.baidu.com',
        # 'u' : 'http://ks.baidu.com/?urbid=/_4__0&bck=0&lfr=1',
        'token' : tokenVal,
        # 'tpl' : 'pp',
        # 'staticpage' : 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
        # 'isPhone' : 'false',
        # 'apiver' : 'v3',
        # 'callback' : 'bd__cbs__i3bil4',
        # 'tt' : '1460596990809',
        };
    postData = urllib.urlencode(postData)

    #发送登录请求
    loginRequest = urllib2.Request(URL_BAIDU_LOGIN,postData)
    loginRequest.add_header('Accept','*/*')
    loginRequest.add_header('Accept-Encoding','gzip,deflate')
    loginRequest.add_header('Accept-Language','zh-CN')
    loginRequest.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 18.0; Windows NT 6.2; Win64; x64;)')
    # loginRequest.add_header('User-Agent','Mozilla/5.0 (iPhone7; CPU iPhone7 OS 9_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/7.0 Mobile/10A403 Safari/8536.25')
    loginRequest.add_header('Content-Type','application/x-www-form-urlencoded')
    sendPost = urllib2.urlopen(loginRequest)
