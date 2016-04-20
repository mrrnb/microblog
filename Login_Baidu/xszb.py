#/usr/bin/env python
#coding: utf-8
#Author: Ezreal
#email: osatmnzn@vip.qq.com
#date: 2016.02.25
#version: 1.0

import urllib2
import bs4
import sys
import requests

reload(sys)
sys.setdefaultencoding('utf-8')
# print sys.getdefaultencoding()

def get_urls(key_word):
    r = requests.get("http://shucheng.baidu.com/search?keyword="+key_word)
    s = bs4.BeautifulSoup(r.text,'html.parser')
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
            s = bs4.BeautifulSoup(r.text,'html.parser')
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
                x = int(raw_input("Check and Choose one!\n[and if NOT in this list input 0 exit]: "))
                # x = 1
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

def get_content(urlno,num_s=1,num_e=5):
    title,content =[],[]
    for i in range(num_s,num_e):
        # payload = {'bkid':url,'crid':i}
        # r = requests.get('http://ks.baidu.com/book/read',params=payload)
        # s = bs4.BeautifulSoup(r.text,'html.parser')
        url = 'http://ks.baidu.com/book/read?bkid=%s&crid=%s&pgsizetype=3'%(urlno,i)
        url_data = urllib2.urlopen(url).read()
        s = bs4.BeautifulSoup(url_data,'html.parser')
        links1 = s.find_all(name ='div',attrs={'class':'dk_bar_sy3'})
        links2 = s.find_all(name ='div',attrs={'class':'dk_content10'})
        links3 = s.find_all(name='div', attrs={'class': 'dk_div_line'}, limit=1)
        logined_name =links3[0].get_text()[:-11]
        if links1 != []:
            # print links1[0].p.get_text()
            title.append(links1[0].p.get_text())
            content.append(links2[0].p.get_text())
        else:
            print 'Only %s page can be download!!'%(i-1)
            break
    print logined_name
    li = [title,content]
    return li
