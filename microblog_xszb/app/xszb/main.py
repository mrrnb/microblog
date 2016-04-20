# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib
import re
import bs4
import requests

URL_BAIDU_INDEX = u'http://www.baidu.com/'
#https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true 也可以用这个
URL_BAIDU_TOKEN = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'
# URL_BAIDU_LOGIN = 'https://passport.baidu.com/v2/?login&u=http%3A%2F%2Fks.baidu.com%2F%3Fbck%3D0%26lfr%3D1'
URL_BAIDU_LOGIN = 'http://wappass.baidu.com/passport/login?tpl=bdbook&u=http%3A%2F%2Fks.baidu.com%2F%3Furbid%3D%2F_4__0%26bck%3D0%26lfr%3D1'
#设置用户名、密码
username = 'mingruirui'
password = 'bdszjszrj,2015'
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
    'u' : 'http%3A%2F%2Fks.baidu.com%2F%3Furbid%3D%2F_4__0%26bck%3D0%26lfr%3D1',
    'tpl' : 'pp',
    'token' : tokenVal,
    'staticpage' : 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
    'isPhone' : 'false',
    'apiver' : 'v3',
    'callback' : 'bd__cbs__i3bil4',
    'tt' : '1460596990809',
    };
postData = urllib.urlencode(postData)

#发送登录请求
loginRequest = urllib2.Request(URL_BAIDU_LOGIN,postData)
loginRequest.add_header('Accept','*/*')
loginRequest.add_header('Accept-Encoding','gzip,deflate')
loginRequest.add_header('Accept-Language','zh-CN')
loginRequest.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)')
loginRequest.add_header('Content-Type','application/x-www-form-urlencoded')
sendPost = urllib2.urlopen(loginRequest)

# #查看贴吧个人主页 ，测试是否登陆成功，由于cookie自动管理，这里处理起来方便很多
# #http://tieba.baidu.com/home/main?un=XXXX&fr=index 这个是贴吧个人主页，各项信息都可以在此找到链接
# teibaUrl = 'http://tieba.baidu.com/f/like/mylike'
# content = urllib2.urlopen(teibaUrl).read();
# content = content.decode('gbk').encode('utf8');
#
# #解析数据，用的BeautifulSoup4，感觉没有jsoup用的爽
# soup = bs4.BeautifulSoup(content,"html.parser");
# list = soup.findAll('tr');
# list = list[1:len(list)];
# careTeibalist = [];
# print '贴吧链接\t吧名\t等级';
# for elem in list:
#     soup1 = bs4.BeautifulSoup(str(elem),'html.parser');
#     print 'http://tieba.baidu.com/'+soup1.find('a')['href']+'\t'+soup1.find('a')['title']+'\t'+soup1.find('a',{'class','like_badge'})['title'];


# teibaUrl = 'https://passport.baidu.com/v2/?login&u=http%3A%2F%2Fks.baidu.com%2F%3Fbck%3D0%26lfr%3D1'
# content = urllib2.urlopen(teibaUrl).read()

# def get_content(blog,num=5):
blog = '35184'
num = 200
title, content = [], []
for i in range(1, num):
    # payload = {'bkid': blog, 'crid': i, 'pgsizetype': 3}
    url = 'http://ks.baidu.com/book/read?bkid=%s&crid=%s&pgsizetype=3'%(blog,i)
    # print url
    # teibaUrl = 'http://index.baidu.com/?tpl=trend&word={0}'.format(key)
    # r = urllib2.Request(url, post_data)
    # rsp = self.opener.open(r).read()
    # r = requests.get('http://ks.baidu.com/book/read', params=payload)
    data = urllib2.urlopen(url).read()
    # data = data.decode('utf-8').encode('utf8')
    # print data
    # s = bs4.BeautifulSoup(r.text, 'html.parser')
    s = bs4.BeautifulSoup(data, 'html.parser')
    links1 = s.find_all(name='div', attrs={'class': 'dk_bar_sy3'})
    links2 = s.find_all(name='div', attrs={'class': 'dk_content10'})
    links3 = s.find_all(name='div', attrs={'class': 'dk_div_line'}, limit=1)
    # print s.find_all(text='mingruirui[')
    logined_name =links3[0].get_text()[0:10]
    print logined_name
    if links1 != []:
        title.append(links1[0].p.get_text())
        content.append(links2[0].p.get_text())
    else:
        print 'Only %s page can be download!!' % (i - 1)
        break
li = [title, content]
for x in range(len(li[0])):
    print li[0][x],li[1][x]

# get_content('74850072',2)