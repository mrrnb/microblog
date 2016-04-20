#coding:utf8

import cookielib
import urllib2, urllib
import os,sys,socket,re
import requests
from bs4 import BeautifulSoup

#解析有多少页博客
pageStr = """var PagerInfo = {\s*allCount\s*:\s*'(\d+)',\s*pageSize\s*:\s*'(\d+)',\s*curPage\s*:\s*'\d+'\s*};"""
pageObj = re.compile(pageStr, re.DOTALL)


#获取登陆token
login_tokenStr = '''bdPass.api.params.login_token='(.*?)';'''
login_tokenObj = re.compile(login_tokenStr,re.DOTALL)

#获取博客标题和url
blogStr = r'''<div><p><a href=".*?">.*?</a></div><a href="(.*?)">(.*?)</a><p></div>'''
blogObj = re.compile(blogStr,re.DOTALL)

class Baidu(object):
    def __init__(self,user = '', psw = '', blog = ''):
        self.user = user
        self.psw  = psw
        self.blog = blog
        if not user or not psw or not blog:
            print "Plz enter enter 3 params:user,psw,blog"
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
        self.opener.addheaders = [('User-agent','Opera/9.23')]
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
            # print rsp
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
                                              # 'staticpage':'https://passport.baidu.com/v2Jump.html',
                                              # 'staticpage':'https://passport.baidu.com/v2/?login',
                                              'staticpage':'https://passport.baidu.com/v2/api/?login',
                                              'tpl':'mn',
                                              'u':'http://ks.baidu.com',
                                              'verifycode':'',
                                            })
                #path = 'http://passport.baidu.com/?login'
                path = 'http://passport.baidu.com/v2/api/?login'
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
                self.opener.addheaders = [('User-agent','Opera/9.23')]
                urllib2.install_opener(self.opener)
                headers = {
                  "Accept": "image/gif, */*",
                  "Referer": "https://passport.baidu.com/v2/?login&u=http%3A%2F%2Fks.baidu.com%2F%3Flfr%3D1",
                  "Accept-Language": "zh-cn",
                  "Content-Type": "application/x-www-form-urlencoded",
                  "Accept-Encoding": "gzip, deflate",
                  "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
                  "Host": "passport.baidu.com",
                  "Connection": "Keep-Alive",
                  "Cache-Control": "no-cache"
                }
                req = urllib2.Request(path,
                                post_data,
                                # headers=headers,
                                )
                rsp = self.opener.open(req).read()
                print rsp
                self.cj.save(self.cookiename)
                #for login test
                #qurl = '''http://hi.baidu.com/pub/show/createtext'''
                #rsp = self.opener.open(qurl).read()
                #file_object = open('login.txt', 'w')
                #file_object.write(rsp)
                #file_object.close()
                req = urllib2.Request('http://ks.baidu.com')
                rsp = self.opener.open(req).read()
                print rsp
            else:
                print "Login Fail"
                sys.exit(0)

    def get_content(self,blog,num=5):
        title, content = [], []
        self.cj.revert(self.cookiename)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [('User-agent','Opera/9.23')]
        urllib2.install_opener(self.opener)
        socket.setdefaulttimeout(30)
        for i in range(1, num):
            # payload = {'bkid': blog, 'crid': i, 'pgsizetype': 3}
            url = 'http://ks.baidu.com/book/read?'
            post_data = urllib.urlencode({
                'bkid':blog,
                'crid':i,
                'pgsizetype': 3
            })
            r = urllib2.Request(url, post_data)
            # print r
            # rsp = urllib2.urlopen(r).read()
            rsp = self.opener.open(r).read()
            # print rsp
            # r = requests.get('http://ks.baidu.com/book/read', params=payload)
            s = BeautifulSoup(rsp, 'html.parser')
            links1 = s.find_all(name='div', attrs={'class': 'dk_bar_sy3'})
            links2 = s.find_all(name='div', attrs={'class': 'dk_content10'})
            links3 = s.find_all(name='div', attrs={'class': 'dk_div_line'}, limit=1)
            # links3 = s.find_all(name='div', attrs={'class': 'dk_login_title'})
            print s.find_all(text='mingruirui')
            print links3[0].get_text()
            if links1 != []:
                title.append(links1[0].p.get_text())
                content.append(links2[0].p.get_text())
            else:
                print 'Only %s page can be download!!' % (i - 1)
                break
        li = [title, content]
        for x in range(len(li[0])):
            print li[0][x],li[1][x]
        return li


    #获取博客一共有多少页，如果有私有博文的话，登陆和不登陆获取的是不一样的
    def getTotalPage(self):
        #获取博客的总页数
        req2 = urllib2.Request(self.blog)
        rsp = urllib2.urlopen(req2).read()
        if rsp:
            rsp = rsp.replace('\r','').replace('\n','').replace('\t','')
            matched_objs = pageObj.findall(rsp)
            if matched_objs:
                obj0,obj1 = matched_objs[0]
                self.allCount = int(obj0)
                self.pageSize = int(obj1)
                self.totalpage = (self.allCount / self.pageSize) + 1
                print 'allCount:%d, pageSize:%d, totalpage:%d' % (self.allCount,self.pageSize,self.totalpage)

    #获取每一页里的博客链接
    def fetchPage(self,url):
        req = urllib2.Request(url)
        rsp = urllib2.urlopen(req).read()
        if rsp:
            rsp = rsp.replace('\r','').replace('\n','').replace('\t','')
            matched_objs = blogObj.findall(rsp)
            if matched_objs:
                for obj in matched_objs:
                    #这里可以用多线程改写一下,单线程太慢
                    self.download(obj[0],obj[1])
    def downloadBywinget(self,url,title):
        #比如使用wget之类的第三方工具，自己填参数写
        pass

    #下载博客
    def download(self,url,title):
        path = '%s/%s.html' % (self.user,title.decode('utf-8'))
        url = 'http://hi.baidu.com%s' % (url)
        print "Download url %s" % (url)
        nFail = 0
        while nFail < 5:
            try:
                sock = urllib.urlopen(url)
                htmlSource = sock.read()
                myfile = file(path,'w')
                myfile.write(htmlSource)
                myfile.close()
                sock.close()
                return
            except:
                nFail += 1
        print ('download blog fail:%s' % (url))

    def dlownloadall(self):
        for page in range(1,self.totalpage+1):
            url = "%s?page=%d" % (self.blog,page)
            #这里可以用多线程改写一下,单线程太慢
            self.fetchPage(url)

def main():
    user = 'mingruirui'       #你的百度登录名
    psw  = 'bdszjszrj,2015'  #你的百度登陆密码,不输入用户名和密码，得不到私有的文章
    blog = "http://ks.baidu.com/book?bkid=74850072" #你自己的百度博客链接
    url = "74850072" #你自己的百度博客链接
    baidu = Baidu(user,psw,blog)
    baidu.login()
    baidu.getTotalPage()
    baidu.dlownloadall()
    baidu.get_content(url,2)
if __name__ == '__main__':
    main()