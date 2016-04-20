#/usr/bin/env python
#coding: utf-8
#Author: Ezreal
#email: osatmnzn@vip.qq.com
#date: 2016.02.25
#version: 1.0

# from __future__ import unicode_literals
from bs4 import BeautifulSoup
import sys
import requests
# import codecs

reload(sys)
sys.setdefaultencoding('utf-8')
# print sys.getdefaultencoding()

def get_urls(key_word):
    r = requests.get("http://shucheng.baidu.com/search?keyword="+key_word)
    s = BeautifulSoup(r.text,'html.parser')
    links0 = s.find_all(name ='div',attrs={'class':'dk_pager'})
    links1 = s.find_all(name ='div',attrs={'class':'dk_content'})
    all_list = []
    tmp_li = []
    x = 0

    if links0 != []:
        tmp_text1 = links0[0].span.get_text()
        tmp_m = tmp_text1.find('/')
        tmp_n = tmp_text1.find(')')
        times = int(tmp_text1[tmp_m+1:tmp_n])
        for i in range(times):
            r = requests.get("http://shucheng.baidu.com/search?keyword="+key_word+"&pg=" + str(i+1))
            s = BeautifulSoup(r.text,'html.parser')
            links1 = s.find_all(name ='div',attrs={'class':'dk_content'})
            for j in range(len(links1)):
                a = links1[j].a.get('href')
                m = a.find('bkid=')
                n = a.find('&',m)
                mn = a[m+5:n]
                tmp_li.append(mn)
                all_list.append('[ %2s ]: %-11s, %s'%(j+(i)*20+1,mn,links1[j].a.get_text()))
    else:
        for j in range(len(links1)):
            a = links1[j].a.get('href')
            m = a.find('bkid=')
            n = a.find('&',m)
            mn = a[m+5:n]
            tmp_li.append(mn)
            all_list.append('[ %2s ]: %-11s, %s'%(j+1,mn,links1[j].a.get_text()))

    if len(tmp_li)>1:
        print '\n'.join(all_list)
        running = True
        while running:

            try:
                # x = int(raw_input("Check and Choose one!\n[and if NOT in this list input 0 exit]: "))
                x = 1
            except:
                print "Input ERROR ! Input Again !"
                continue
            if x >= 1 and x <= len(all_list)+1:
                return tmp_li[x-1]
                running = False
            elif x==0:
                sys.exit()
            else:
                print "NUMBER ERROR ! Input Again !"
    else:
        return tmp_li[x-1]


def get_content(url,num=5):
    title,content =[],[]
    for i in range(1,num):
        payload = {'bkid':url,'crid':i,'pgsizetype':3}
        r = requests.get('http://ks.baidu.com/book/read',params=payload)
        s = BeautifulSoup(r.text,'html.parser')
        links1 = s.find_all(name='div', attrs={'class': 'dk_bar_sy3'})
        links2 = s.find_all(name='div', attrs={'class': 'dk_content10'})
        links3 = s.find_all(name='div', attrs={'class': 'dk_div_line'},limit=1)
        # links3 = s.find_all(name='div', attrs={'class': 'dk_login_title'})
        print links3[0].get_text()
        if links1 != []:
            title.append(links1[0].p.get_text())
            content.append(links2[0].p.get_text())
        else:
            print 'Only %s page can be download!!'%(i-1)
            break
    li = [title,content]
    return li