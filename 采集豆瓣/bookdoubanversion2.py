# -*- coding:UTF-8 -*-
#Author:周文康
import time
import requests
import sys
from bs4 import BeautifulSoup
import threading
import Queue
import random
import codecs
import json
start = time.clock()
reload(sys)
sys.setdefaultencoding('utf-8')



# Message()

class Message:
    def __init__(self,name,book_image,content,booktags,star_dicts,rate_num,rate_peo):
       self.name=name
       self.book_image=book_image
       self.content=content
       self.booktags=booktags
       self.star_dicts=star_dicts
       self.rate_num=rate_num
       self.rate_peo=rate_peo
    def packdd(self):
       print '123'
       dicts = {}
       dicts["bookname"]=self.name
       dicts["book_image"]=self.book_image
       dicts["content_intro"]=self.content
       dicts["booktags"]=self.booktags
       dicts["rate"]={}
       dicts["rate"]['rate_num']=self.rate_num
       dicts["rate"]['rate_peo']=self.rate_peo
       dicts["rate"]['rate_star']={}
       dicts["rate"]['rate_star']=self.star_dicts
       return dicts

#信息返回格式
#{"bookname":"xxx","book_image":"xxxx","content_intro":"xxx","booktags":"xxx","rate":{"rate_num":"xxx","rate_peo":"xxx","rate_star":{"star_five":"xxx","star_four":"xxx","star_three":"xxx","star_two":"xxx","star_one":"xxx"}}}

end = time.clock()
print 'Running time: %s Seconds'%(end-start)

def getHtmlInfo(urls):
    #简单获取
    ##
    # f = codecs.open('hahaha.html','a+',encoding='UTF-8')
    headers = [
           {'User-Agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
           {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
           {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
           {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    # url = u'https://book.douban.com/subject/'+str(ids)
    ContentPage_Info = requests.get(urls,headers=random.choice(headers))
    end = time.clock()
    print 'GetPage time: %s Seconds'%(end-start)
    return ContentPage_Info

    #计算网页获取速度
def HandleInfo(ContentPage_Info):
    Page_Html = BeautifulSoup(ContentPage_Info.content)
    #bookname
    bookname = Page_Html.title.string
    #bookimage
    book_image = Page_Html.select('#mainpic > a')[0].attrs['href']
    
    #书本信息处理后
    content = Page_Html.select("#info")[0].get_text().replace('-',':').replace(' ','').replace('\n','-').replace('---','').replace('--','-')
    booktags = Page_Html.select('#db-tags-section .indent > span')
    bookt = []
    for i in xrange(len(booktags)):
        bookt.append(booktags[i].get_text().replace(' ','').replace('\n','').replace(u'\xa0',u''))
    booktags = ','.join(bookt)
    # 书本标签    

    #评分人数
    rete_peo = Page_Html.select('#interest_sectl > div > div > strong')[0].get_text()

    #评分
    rate_num= Page_Html.select('#interest_sectl .rating_sum > span > a > span')[0].get_text()

    Page_Htmls = Page_Html.find('div',id='interest_sectl')
    Star_Info  = Page_Htmls.find_all("span")
    star_list=['star_five','star_four','star_three','star_two','star_one']
    rate_list=[]
    for i in xrange(3,len(Star_Info)):
        if not i%2:
            rate_list.append(Star_Info[i].get_text().replace('\n','').replace(' ',''))

    #星星 
    dicts = dict(zip(star_list,rate_list))
    try:
        content = Page_Html.select('#link-report > div .intro')[0].get_text().replace('\n','')
    except IndexError:
        content=Page_Html.select('.short .intro')[0].get_text().replace('\n','')

    #书本简要描述

    aa = Message(bookname,book_image,content,booktags,dicts,rate_num,rete_peo)
    ccc = aa.packdd()
    return ccc

# aaaa = getHtmlInfo(26835689)
# ffff = HandleInfo(aaaa)
# f = open('hahaha.txt','a+')
# f.write(json.dumps(ffff,ensure_ascii=False)+'\n')
# f.close()
def GetId(pageUrl):
    
    sss = requests.get(pageUrl)
    # print sss.content
    ddd = BeautifulSoup(sss.content)
    ccc = ddd.select('.subject-item .info > h2 > a')
    for i in xrange(len(ccc)):
        eee = getHtmlInfo(ccc[i].attrs["href"])
        aaa = HandleInfo(eee)
        f = open('hahaha.txt','a+')
        f.write(json.dumps(aaa,ensure_ascii=False)+'\n')
        f.close()
GetId(u'https://book.douban.com/tag/%E9%9A%8F%E7%AC%94')