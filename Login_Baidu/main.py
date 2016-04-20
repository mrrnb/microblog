# coding: utf-8
# Author: Ezreal
# email: osatmnzn@vip.qq.com
# date: 2016.04.19
# version: 1.0

from login import baiduLogin
from xszb import get_content,get_urls
import urllib2
import bs4


def main():
    name = 'xsname'
    zhang_s = 1
    zhang_e = 10
    username = 'mingruirui'
    password = ''
    name_gbk = name.decode('utf-8').encode('gbk')
    baiduLogin(username,password,True)
    # baiduLogin(username,password)
    xxx = get_urls(name)
    li = get_content(xxx,zhang_s,zhang_e+1)
    if li != [[],[]]:
        f = open('NOVEL/'+name_gbk+'.txt', 'w')
        f.write(name + '\r\r')
        for i in range(len(li[0])):
            f.write(li[0][i] + '\r\r')
            f.write(li[1][i] + '\r\r\r')
        f.close()
    else:
        print "Can not get this one!"


    #查看贴吧个人主页 ，测试是否登陆成功，由于cookie自动管理，这里处理起来方便很多
    #http://tieba.baidu.com/home/main?un=XXXX&fr=index 这个是贴吧个人主页，各项信息都可以在此找到链接
    teibaUrl = 'http://tieba.baidu.com/f/like/mylike'
    content = urllib2.urlopen(teibaUrl).read();
    content = content.decode('gbk').encode('utf8');

    #解析数据，用的BeautifulSoup4，感觉没有jsoup用的爽
    soup = bs4.BeautifulSoup(content,"html.parser");
    list = soup.findAll('tr');
    list = list[1:len(list)];
    careTeibalist = [];
    print '贴吧链接\t吧名\t等级';
    for elem in list:
        soup1 = bs4.BeautifulSoup(str(elem),'html.parser');
        text1 = soup1.find('a')['href']
        text2 = soup1.find('a')['title']
        text3 = soup1.find('a',{'class','like_badge'})['title']
        print 'http://tieba.baidu.com/'+text1+'\t'+text2+'\t'+text3

if __name__=='__main__':
    main()