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
start = time.clock()
reload(sys)
sys.setdefaultencoding('utf-8')


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
s = requests.get(u'https://book.douban.com/subject/26835689/?icn=index-editionrecommend',headers=random.choice(headers))


end = time.clock()
print 'GetPage time: %s Seconds'%(end-start)
#计算网页获取速度

sss = BeautifulSoup(s.content)
bookname = sss.title.string
print sss.select('#mainpic > a')[0].attrs['href']
#bookimage


ttt = sss.select("#info")
content = ttt[0].get_text().replace('-',':').replace(' ','').replace('\n','-').replace('---','').replace('--','-')
#书本信息处理后


#评分人数
rete_peo = sss.select('#interest_sectl > div > div > strong').get_text()

#评分
rate_num= sss.select('#interest_sectl .rating_sum > span > a > span').get_text()

ssss = sss.find('div',id='interest_sectl')
dd  = ssss.find_all("span")
rate_list=[]
for i in xrange(3,len(dd)):
    if not i%2:
        rate_list.append(dd[i].get_text().replace('\n','').replace(' ',''))
#星星 

content = sss.select('#link-report > div .intro')[0].get_text()
#书本简要描述
booktags = sss.select('#db-tags-section .indent > span')
bookt = []
for i in xrange(len(booktags)):
    bookt.append(booktags[i].get_text().replace(' ','').replace('\n','').replace(u'\xa0',u''))
booktags = ','.join(bookt)
# 书本标签
# Message()

class Message:
    def __init__(self,name,content,booktags,rate_list,rate_num,rate_peo):
        self.name=name
        self.content=content
        self.booktags=booktags
        self.rate_list=rate_list
        self.rate_num=rate_num
        self.rate_peo=rate_peo
    def pack(self):
        dicts = {}
        dicts["bookname"]=self.name
        dicts["content_intro"]=self.content
        dicts["booktags"]=self.booktags
        dicts["rate"]={}
        dicts["rate"]['rate_num']=self.rate_num
        dicts["rate"]['rate_peo']=self.rate_peo
        dicts["rate"]['rate_star']={}
        dicts["rate"]['rate_star']=self.rate_list
        return dicts

#信息返回格式
#{"bookname":"xxx","content_intro":"xxx","booktags":"xxx","rate":{"rate_num":"xxx","rate_peo":"xxx","rate_star":{"star_five":"xxx","star_four":"xxx","star_three":"xxx","star_two":"xxx","star_one":"xxx"}}}

end = time.clock()
print 'Running time: %s Seconds'%(end-start)