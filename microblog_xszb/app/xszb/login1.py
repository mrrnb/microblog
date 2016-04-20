#coding:utf8

import cookielib
import urllib2, urllib
import os,sys,socket,re

#获取登陆token
login_tokenStr = '''bdPass.api.params.login_token='(.*?)';'''
login_tokenObj = re.compile(login_tokenStr,re.DOTALL)

class Baidu(object):
    # def __init__(self,user = '', psw = '', blog = ''):
    def __init__(self, user='', psw=''):
        self.user = user
        self.psw  = psw
        # self.blog = blog
        # if not user or not psw or not blog:
        if not user or not psw:
            # print "Plz enter enter 3 params:user,psw,blog"
            print "Plz enter enter 2 params:user,psw"
            sys.exit(0)
        if not os.path.exists(self.user):
            os.mkdir(self.user)
        self.cookiename = 'baidu%s.coockie' % (self.user)
        self.token = ''
        self.allCount  = 0
        self.pageSize  = 10
        self.totalpage = 0
        self.logined = False
        self.cj = cookielib.LWPCookieJar()
        try:
            self.cj.revert(self.cookiename)
            # self.logined = True
            print "OK"
        except Exception, e:
            print e
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        # self.opener.addheaders = [('User-agent','Opera/9.23')]
        urllib2.install_opener(self.opener)
        socket.setdefaulttimeout(30)
    #登陆百度
    def login(self):
        #如果没有获取到cookie，就模拟登陆
        if not self.logined:
            print "logon to baidu ..."
            #第一次先访问一下，目的是为了先保存一个cookie下来
            qurl = '''https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false'''
            r = self.opener.open(qurl)
            self.cj.save(self.cookiename)
            #第二次访问，目的是为了获取token
            qurl = '''https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false'''
            r = self.opener.open(qurl)
            rsp = r.read()
            #print rsp
            self.cj.save(self.cookiename)
            #通过正则表达式获取token
            matched_objs = login_tokenObj.findall(rsp)
            if matched_objs:
                self.token = matched_objs[0]
                print 'token =', self.token
                #然后用token模拟登陆
                post_data = urllib.urlencode({'username':self.user,
                                              'password':self.psw,
                                              'token':self.token,
                                              'charset':'UTF-8',
                                              'callback':'parent.bd12Pass.api.login._postCallback',
                                              'index':'0',
                                              'isPhone':'false',
                                              'mem_pass':'on',
                                              'loginType':'1',
                                              'safeflg':'0',
                                              'staticpage':'https://passport.baidu.com/v2Jump.html',
                                              'tpl':'mn',
                                              'u':'http://www.baidu.com/?&lfr=1',
                                              'verifycode':'',
                                            })
                path = 'http://passport.baidu.com/v2/api/?login'
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
                self.opener.addheaders = [('User-agent','Opera/9.23')]
                urllib2.install_opener(self.opener)
                headers = {
                  "Accept": "image/gif, */*",
                  # "Referer": "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F",
                  # "Referer": "https://passport.baidu.com/v2/?login&u=http%3A%2F%2Fks.baidu.com%2F%3Flfr%3D1",
                  "Referer": "http://ks.baidu.com/book/read?bkid=35184&crid=1&pgsizetype=3",
                  "Accept-Language": "zh-cn",
                  "Content-Type": "application/x-www-form-urlencoded",
                  "Accept-Encoding": "gzip, deflate",
                  "User-Agent": "Mozilla/4.0 (compatible; MSIE 12.0; Windows NT 6.1;)",
                  "Host": 'http://wappass.baidu.com/passport/login',
                  "Connection": "Keep-Alive",
                  "Cache-Control": "no-cache"
                }
                req = urllib2.Request(path,
                                post_data,
                                headers=headers,
                                )
                # rsp = self.opener.open(req).read()
                self.cj.save(self.cookiename)
            else:
                print "Login Fail"
                sys.exit(0)

def main():
    user = 'mingruirui'       #你的百度登录名
    psw  = 'bdszjszrj,2015'  #你的百度登陆密码,不输入用户名和密码，得不到私有的文章
    # blog = "http://hi.baidu.com/osatmnzn" #你自己的百度博客链接
    # baidu = Baidu(user,psw,blog)
    baidu = Baidu(user, psw)
    baidu.login()
    # baidu.getTotalPage()
    # baidu.dlownloadall()
if __name__ == '__main__':
    main()